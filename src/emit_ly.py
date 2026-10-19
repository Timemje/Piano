"""LilyPond exporter: emits music.ly from the measure data (the source strings
are themselves a strict LilyPond subset, so the notes pass through verbatim)."""

HEADER = r'''\version "2.24.0"

\header {
  title = "An Unfinished Grief"
  subtitle = "Concert Prelude for Solo Piano"
  subsubtitle = "in C-sharp minor"
  tagline = ##f
}

\paper {
  #(set-paper-size "a4")
  top-margin = 13\mm
  bottom-margin = 13\mm
  left-margin = 15\mm
  right-margin = 15\mm
  system-system-spacing = #'((basic-distance . 15) (minimum-distance . 11) (padding . 2.5) (stretchability . 12))
  markup-system-spacing.padding = #3
  ragged-last-bottom = ##t
  ragged-bottom = ##f
  print-first-page-number = ##f
  oddHeaderMarkup = \markup \fill-line { "" \unless \on-first-page \fromproperty #'page:page-number-string }
  evenHeaderMarkup = \markup \fill-line { \unless \on-first-page \fromproperty #'page:page-number-string "" }
}

#(set-global-staff-size 18.5)

global = { \key cis \minor \time 4/4 }
'''

LAYOUT = r'''
  \layout {
    \context {
      \Score
      \override SpacingSpanner.base-shortest-duration = #(ly:make-moment 1/16)
      \override MetronomeMark.padding = #2
      \override BarNumber.break-visibility = #end-of-line-invisible
      barNumberVisibility = #first-bar-number-invisible-save-broken-bars
    }
    \context {
      \PianoStaff
      \override StaffGrouper.staff-staff-spacing = #'((basic-distance . 12) (minimum-distance . 8) (padding . 2) (stretchability . 6))
    }
    \context {
      \Dynamics
      \override TextScript.font-shape = #'italic
      \override DynamicLineSpanner.staff-padding = #1.5
    }
    \context {
      \Voice
      \override TextScript.font-shape = #'italic
      \override BreathingSign.text = \markup \musicglyph "scripts.caesura.straight"
      %%HOOK%%
    }
  }
'''

# Event dump used only by the validator: LilyPond reports every note/rest it
# actually parsed, with spelled pitch, staff and timing.
DUMP_ENGRAVER = r'''
#(define dump-port (open-output-file "lily_events.tsv"))
#(define (dump-ev kind)
   (lambda (engraver event)
     (let* ((ctx (ly:translator-context engraver))
            (staff (ly:context-find ctx 'Staff))
            (sid (if staff (ly:context-id staff) "?"))
            (mom (ly:context-current-moment ctx))
            (p (ly:event-property event 'pitch))
            (d (ly:event-property event 'duration)))
       (format dump-port "~a\t~a\t~a\t~a\t~a\t~a\t~a\t~a\n"
               kind sid (ly:context-id ctx)
               (ly:moment-main mom)
               (if (ly:pitch? p) (ly:pitch-notename p) "-")
               (if (ly:pitch? p) (ly:pitch-alteration p) "-")
               (if (ly:pitch? p) (ly:pitch-octave p) "-")
               (ly:moment-main (ly:duration-length d)))
       (force-output dump-port))))
#(define dump-note (dump-ev "note"))
#(define dump-rest (dump-ev "rest"))
#(define dump-engraver
   (make-engraver
     (listeners
       (note-event . dump-note)
       (rest-event . dump-rest))))
'''


def _voice_body(measures, vid, other):
    parts = []
    for m in measures:
        s = m.src[vid]
        o = m.src[other]
        if s is None:
            body = "s1"
        else:
            body = ("\\voiceOne " if vid in ("RA", "LA") else "\\voiceTwo ") + s if o is not None \
                else "\\oneVoice " + s
        parts.append(f"  % m.{m.num}\n  {body} |")
    return "\n".join(parts)


# System and page breaks chosen at phrase boundaries; page turns fall where a
# hand is free (m. 16 fermata, m. 54 RH tacet, m. 72 rests).
SYSTEMS = {5, 9, 13, 21, 25, 29, 33, 37, 41, 44, 47, 50, 52, 57, 61, 65, 69, 77}
PAGES = {17, 54, 73}


def _line_body(measures, vid, prefix="", breaks=False):
    parts = []
    for m in measures:
        s = m.src[vid] or "s1"
        if breaks and m.num in PAGES:
            s = "\\pageBreak " + s
        elif breaks and m.num in SYSTEMS:
            s = "\\break " + s
        parts.append(f"  % m.{m.num}\n  {s} |")
    return prefix + "\n".join(parts)


def render(measures, hook=False):
    out = []
    if hook:
        out.append(DUMP_ENGRAVER)
    out.append(HEADER)
    out.append("rightA = {\n" + _voice_body(measures, "RA", "RB") + "\n}\n")
    out.append("rightB = {\n" + _voice_body(measures, "RB", "RA") + "\n}\n")
    out.append("leftA = {\n" + _voice_body(measures, "LA", "LB") + "\n}\n")
    out.append("leftB = {\n" + _voice_body(measures, "LB", "LA") + "\n}\n")
    out.append("marks = {\n" + _line_body(measures, "MK", breaks=True) + '\n  \\bar "|."\n}\n')
    out.append("dyns = {\n" + _line_body(measures, "DYN") + "\n}\n")
    out.append("peds = {\n  \\set Dynamics.pedalSustainStyle = #'mixed\n"
               + _line_body(measures, "PED") + "\n}\n")
    score = r'''
\score {
  \new PianoStaff <<
    \new Staff = "up" <<
      \global
      \new Voice = "RA" \rightA
      \new Voice = "RB" \rightB
      \new Voice = "MK" \marks
    >>
    \new Dynamics \dyns
    \new Staff = "down" <<
      \global
      \clef bass
      \new Voice = "LA" \leftA
      \new Voice = "LB" \leftB
    >>
    \new Dynamics \peds
  >>
''' + LAYOUT.replace("%%HOOK%%", r"\consists #dump-engraver" if hook else "") \
        + ("  \\midi { }\n" if hook else "") + "}\n"
    out.append(score)
    return "\n".join(out)
