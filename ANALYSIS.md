# An Unfinished Grief — Concert Prelude for Solo Piano

C-sharp minor · 4/4 · Largo doloroso, quarter = 56 · 80 measures · measured MIDI playback 5:52

Deliverables: `music.pdf` (engraved score, 6 pp.), `music.ly` (LilyPond source),
`music.mxl` (compressed MusicXML 4.0), `music.midi` (performance render),
`validation_report.txt` (measured validation results), plus `music_preview.mp3`
(FluidSynth / GM-piano audio preview of the MIDI, for listening only).

Source of truth: `src/sec_a.py … sec_d.py` (each voice of each bar written in a strict subset
of LilyPond syntax), parsed by `src/notation.py` into one event model. `src/emit_ly.py`,
`src/emit_xml.py` and `src/emit_midi.py` export from that model; `src/validate.py` checks
everything. Rebuild: `python3 src/build.py . && lilypond -o music music.ly && python3 src/validate.py .`

---

## 1. Stage 1 design (made before any notes were entered)

1. **Motif M** — 5–♭6–5–♭3 = G♯–A–G♯–E, rhythm *eighth pickup → dotted quarter (the leaning ♭6) →
   eighth → half*. Short reach, long ache, short release, long fall.
2. **Secondary idea S** — the "reach": three rising eighths from ♭3 (E–F♯–G♯), a leap up to a long
   note (B), and a sigh down (A–G♯). S rises where M falls, and S always ends in M's sigh.
3. **Harmonic question** — the dominant never closes a phrase onto the tonic. Phrase-ending
   dominants are deceptive (V→VI, mm. 7–8, 21–22, 50–51), cut off by silence (mm. 4, 16, 66–67)
   or decay (m. 72). The ♭6 of the motif (A) *is* the root of the deceptive chord, so the
   melodic wound A/G♯ and the harmonic wound V/VI are the same thing.
4. **Tonal regions** — C♯ minor; E major / E minor (III, darkened); German sixth (G♮ → F𝄪);
   a chromatic-mediant chain of dominants G♯7 → B7 → D; F♯ minor, G♯ minor, A, D (applied
   dominants); D minor (Neapolitan minor, temporary key signature), one bar of G minor (tritone
   from the tonic); chromatic return to V.
5. **Bass strategy** — selective low C♯ bell (mm. 1, 57, 60, 68, 73, 76, 79); lament descents
   (C♯–B–A in m. 5–6; full chromatic C♯–B♯–B–A♯–A–G♯ in A′ mm. 64–66); rising chromatic
   bass E♯–F♯–F𝄪–G♯–A in wave 2 and D–D♯–E–E♯–F♯–F𝄪–G♯ into the climax.
6. **Climax preparation** — dominant-ninth arpeggio spelled by wave 1's motif entries; ascending
   diminished-seventh chain mm. 37–40.
7. **Peak event (m. 51)** — V7♭9 with A6 on top (m. 50) moves to A0–A1 in the bass with G♯6 on
   top: the soprano and bass exchange A and G♯. The melody's "resolution" lands as a major
   seventh against the deceptive bass.
8. **A′** — melody of mm. 1–4 returns note-for-note (mm. 60–63) over darkened harmony
   (VI→♭vi with C♮; V→G♯°).
9. **Ending** — the last melodic motion is A→G♯ (♭6→5); the motif's E never returns; final
   sonority a hollow C♯–G♯ fifth, no third, no dominant before it.
10. **Intensity curve** — pp (1–16) · p→mf peak m. 21 · p→f peak m. 31 · mp→ff m. 40 · ff 41–49 ·
    **fff 50–51** · collapse to p by m. 53 · ppp m. 55 · pp–mp–ppp (57–72) · pp→ppp (73–80).

## 2. Architecture

| Section | mm. | What happens |
|---|---|---|
| A — Fragility | 1–16 | M alone over a low C♯ (1–2); S (3–4, two 9–8 sighs); consequent with the first chromatic note, D♮5 (m. 6), and the deceptive cadence (7–8); S in E major darkened to E minor, G♮ respelled F𝄪 in a German sixth (9–12); M augmented over V♭9 (13–14); the dominant fades into a held silence (15–16). |
| B — Accumulation | 17–40 | **Wave 1** (17–24): M sequenced up by thirds on G♯7 → B7 → D (its first notes spell G♯–B♯–D♯–F♯–A), peak mf at m. 21, deceptive VI, tenor/melody imitation, withdrawal. **Wave 2** (25–32): applied-dominant sequence, octaves, rising chromatic bass, peak f at m. 31 (F♯6), D major darkens to D minor. **Wave 3** (33–40): Neapolitan-minor region with rolling arpeggios and an inner lament line, one bar of G minor, *subito p* (m. 36), then a chromatic ascent through three diminished sevenths to V♭9 (ff). |
| C — Breaking point | 41–56 | mm. 1–8 recomposed at full force. *Arrival* (41–45): M with A6 crushed against G♯6 inside the tonic chord; S sung by the bass in octaves; the 9–8 of m. 4 at ff; the Neapolitan D now at the top. *Refusal* (46–50): the turn of m. 7 climbs B♯→D♯→F♯→A over a G♯ pedal for five bars, LH 8ths → triplets → 16ths, top note C♯7 (m. 49), V♭9 fff + caesura. *Break* (51–56): VI maj7 over A0; German sixth (G♯→F𝄪 collapse); texture dismantled in two bars; M sinks into the bass; distant high sigh; silence. |
| A′ — Aftermath | 57–72 | M augmented and incomplete (A never falls); mm. 1–4 return with identical melody and darker harmony (60–63); the consequent over a full chromatic lament breaks off; the deceptive VI never sounds, a fermata rest stands in its place (m. 67); echoes of the collapse (68–69); S contracted to three notes (70); the dominant decays to G♯° (71–72). |
| Coda — Disappearance | 73–80 | 3-note, 2-note, 1-note fragments; bass reduced from octave to fifth to nothing; rests lengthen; ppp; last sigh A4→G♯4 over a hollow C♯2–G♯2; fermata on the sound, then on the silence. |

## 3. Harmonic analysis (every chord named is in the score; pitches spelled)

**(1) Opening, mm. 1–8.** m. 1: C♯1–C♯2 alone. m. 2: A4 sounds over that bare C♯, a ♭6 with no
chord to explain it, then falls to G♯4. On beat 3 the tonic arrives, **C♯ minor (C♯–E–G♯)**,
voiced E3–G♯3–C♯4. m. 3: S rises over the held tonic. On beat 3 the bass drops to A and the
chord becomes **A major add 9 (A–C♯–E–B)**, with B4 as a 9th resolving to A4 (9–8). m. 4: the
bass moves A→G♯ while A4 is held over it. **G♯ major (G♯–B♯–D♯)** with A as a 9–8 suspension,
then F♯4 adds the seventh: **G♯7 (G♯–B♯–D♯–F♯)**. A breath rest follows. m. 5: **C♯ minor** (hollow
fifth C♯2–G♯2 in the bass, C♯4–E4 above), then over bass B, **C♯m7/B (B–C♯–E–G♯)**, under which the displaced motif's A4
is an appoggiatura. m. 6: **A major (A–C♯–E)** → **Neapolitan sixth D/F♯ (F♯–A–D)**. D♮5 is the
first note outside the key, and it sighs to C♯5. m. 7: **G♯7 (G♯–B♯–D♯–F♯)**; the melody
circles the tonic pitch (B♯–C♯–D♯–B♯). m. 8: the question. **A major (A–C♯–E)** replaces
the expected C♯ minor: B♯4→C♯5, F♯→E, D♯→E, G♯→A. Then the alto sighs A4→G♯4, turning the
chord into **A maj7 (A–C♯–E–G♯)**. That sonority returns at the climax.

**(2) First important chromatic transition, mm. 9–13.** m. 9: **E/G♯ (G♯–E–B)**, S in the
relative major. m. 10: **A (A–C♯–E)** → **E/B (B–E–G♯)** → **B7 (B–D♯–F♯–A)**, a cadential
6/4–V7 in E. m. 11: B7 resolves to **E minor/G (G–B–E)**, not E major. G♮ and D♮ enter the
melody (mode mixture; E minor is a chromatic mediant of C♯ minor, sharing only E). m. 12,
*enharmonic reinterpretation*: the bass moves to A, and the G♮ of m. 11 returns respelled as
**F𝄪** in a **German augmented sixth (A–C♯–E–F𝄪)**. Original spelling: G♮ as the third of
E minor. New spelling: F𝄪, the augmented sixth above A, because it now has to rise a semitone
to G♯. The melody reaches it as A4→F𝄪4, a diminished third, so G♯ is pressed from both sides
(A above, F𝄪 below). m. 13: the Ger+6 resolves to the **cadential 6/4 (G♯–C♯–E)**, then to
**G♯7♭9 (G♯–B♯–D♯–F♯–A)**, with A4 as the ninth, held. m. 15: over the G♯ pedal the alto
D♯→D♮ produces **G♯7♭5 (G♯–B♯–D–F♯)**, the same pitches as a French sixth on D.

**(3) Build toward the climax.** *Wave 1, mm. 17–21*: **C♯m** → **G♯7/B♯ (V6/5)** →
**B7 (B–D♯–F♯–A)** → **D/F♯ (F♯–A–D)** → **G♯7♭9**. G♯7→B7 and B→D are chromatic
mediants: major-quality chords a minor third apart with one common tone each (D♯, then F♯),
connected by semitones (B♯→B, G♯→A, D♯→D). The motif's first notes, G♯4, B♯4, D♯5, F♯5 and
then A5 at the peak, spell **G♯–B♯–D♯–F♯–A**. m. 22: deceptive **A maj7**; m. 23: **F♯m7
(F♯–A–C♯–E)**, where the melody imitates the tenor's motif in F♯ minor (C♯–D–C♯–A).
*Wave 2, mm. 25–31*: **C♯7/E♯ (C♯–E♯–G♯–B)** → **F♯m7** | **D♯7/F𝄪 (D♯–F𝄪–A♯–C♯)** →
**G♯m7 (G♯–B–D♯–F♯)** | **E7/G♯ (E–G♯–B–D)** → **A (A–C♯–E)** → **A7 (A–C♯–E–G)** →
**A7/G** → **D/F♯**. Over each applied dominant the motif's upper neighbour is that chord's ♭13 (A over C♯7, B
over D♯7, C♮ over E7, F♮ over A7); the last two are chromatic. The bass rises E♯–F♯–F𝄪–G♯–G♯–A. m. 32: **D minor (D–F–A)** → **A7 (A–C♯–E–G)**.
*Wave 3*: **D minor**, with an inner lament D–C♯–C, giving **D–F–A–C♯** and then **Dm7
(D–F–A–C)** → **B♭ (B♭–D–F)** → **G minor (G–B♭–D)** → **E♭ maj7 (E♭–G–B♭–D)** →
**A7♭9 (A–C♯–E–G–B♭)**. mm. 37–40: **D minor** → **B♯°7/D♯ (D♯–F♯–A–B♯)** → **C♯m/E
(E–G♯–C♯)** → **E♯°7 (E♯–G♯–B–D)** → **F♯ minor (F♯–A–C♯)** → **F𝄪°7 (F𝄪–A♯–C♯–E)** →
**G♯7♭9**. The chord in m. 37 is spelled B♯–D♯–F♯–A rather than D♯–F♯–A–C because it resolves
to C♯ (B♯→C♯), not to E. Spelled with C♮ it would be vii°7 of E. In m. 37 the held A5 changes
role: the fifth of D minor on beat 1, the seventh of B♯°7 on beat 3, then it falls to G♯5 in
m. 38.

**(4) Extended dominant, mm. 46–50.** Five bars over a G♯ pedal. m. 46: **G♯ (G♯–B♯–D♯)**,
with passing F♯. m. 47: **G♯7 (G♯–B♯–D♯–F♯)**; the turn's upper neighbour sounds an
**augmented triad E–G♯–B♯**. m. 48: **G♯7♭9 (G♯–B♯–D♯–F♯–A)**, A6 entering at the top.
m. 49: beat 3 puts **C♯–E–A** (an A major triad, C♯7 on top) above the G♯ bass, so the
deceptive chord is already sounding over the dominant a bar before the bass gives way; beat 4
returns to **D♯–F♯–A** over G♯. m. 50: **G♯7♭9** in full (A5–B♯5–D♯6–F♯6–A6), fff, then a
caesura. Five bars of dominant, each one intensifying (rhythm 8ths → triplets → 16ths, top
rising B♯5 → D♯6 → F♯6 → A6/C♯7), and the bass never moves.

**(5) Climactic arrival, m. 51.** **A major 7 (A–C♯–E–G♯)**: A0–A1 in the bass, E3–A3–C♯4–E4,
and G♯5–A5–C♯6–E6–G♯6 on top. The soprano A6 of m. 50 resolves to G♯6, as a ninth should over
the dominant, but the bass leaves G♯ for A in the same instant. The resolution note becomes a
major seventh against the lowest A on the piano, and G♯5 grinds against A5 inside the right
hand. m. 52: G♯ collapses a semitone to F𝄪: **German sixth (A–C♯–E–F𝄪)**, ff with diminuendo,
over a descending cascade. m. 53: F𝄪→G♯, **G♯ major (G♯–B♯–D♯)**, now p.

**(6) Reharmonised reprise, mm. 60–66.** The melody of mm. 1–4 returns pitch-for-pitch. m. 61:
the A4 that floated over bare C♯ in m. 2 is now the fifth of **D minor over the C♯ pedal
(C♯–D–F–A)**. D and F then sink by semitone to C♯ and E (**C♯ minor**). m. 62: the A major
add 9 of m. 3 becomes **A minor add 9 (A–C–E–B)**: one note changes, C♯→C♮, and the tonic
pitch itself is flattened. m. 63: the dominant of m. 4 (G♯–B♯–D♯) loses its B♯ and D♯:
**G♯ diminished (G♯–B–D)** → **G♯ half-diminished (G♯–B–D–F♯)**. It is still the 9–8 sigh,
over a chord that can no longer lead anywhere. mm. 64–66: the full chromatic lament
C♯–B♯–B–A♯–A–G♯ carries **C♯m** → **B♯°7 (B♯–D♯–F♯–A)**, now with the motif's A as a seventh →
**C♯m/B** → **D augmented over A♯ (D–F♯–A♯)**, the Neapolitan D distorted → **A (A–C♯–E)** →
**G♯7 (G♯–B♯–D♯–F♯)**. m. 67: where VI should arrive there is a fermata rest. Only A3→G♯3
sounds, in the tenor. m. 70: **A–E–G♯** (VI maj7 with no third) under the contracted S.
m. 71: **G♯–B♯–D** (lowered fifth). m. 72: **G♯–B–D**.

**(7) Final gesture, mm. 73–80.** m. 73: **D minor over C♯ (C♯–D–F–A)** on beat 2. D falls to
C♯; F just stops. What remains is the bare **C♯–G♯** fifth. mm. 74–78: A4 hangs over the
ringing C♯ (the dissonance of m. 2 returning) and finally falls to G♯4. mm. 79–80: **C♯2–G♯2
with G♯4**, a hollow fifth with no third, approached by ♭6→5 and not from any dominant. The
E that would complete the motif never comes. The key still reads clearly as C♯ minor (tonic
in the bass, fifth above), but the minor third is missing, and so is any cadence. A fermata on
the sound, then one on the silence.

## 4. How the motif transforms

- **A** — the original fragile statement (mm. 1–2); displaced by two beats (m. 5); augmented
  over V♭9 (mm. 13–14); an inner-voice sigh (alto A4–G♯4, m. 8).
- **B** — expanding and urgent: sequenced up by thirds over chromatic-mediant dominants (17–21);
  passed to the tenor and imitated in F♯ minor (22–23); started on the beat, ending on E♯ over
  C♯7 (25); in octaves on A♯ (27); in diminution (29); transposed exactly into D minor (33)
  and G minor (35); cut down to the obsessive A–B♭ (36).
- **C** — the climactic transformation: opening pitches in five-note fff chords with the ♭6
  crushed against its resolution (41); the 9–8 at the top (43); then the two notes of the
  motif's sigh swap between soprano and bass (50–51); the motif sinks into the bass octaves (54).
- **A′** — exhausted recollection: augmented and incomplete, the A never falls back (57–59);
  identical melody over darker chords (60–63); its continuation stops after the D (65).
- **Coda** — three notes, then two, then one sigh (73–78). The E, M's last note, never returns.

## 5. Revision log

*Stage 3 (musical review)*: mm. 17–20 had four identical LH rhythms. They now have alto
common-tone ties (F♯4, A4) and varied LH rhythm. In wave 2 the LH had been copied from wave 1;
it now has a rocking eighth-note figure that sets it apart. m. 11 LH gets a syncopated entry.
Outer-voice scan found parallel fifths at m. 24 (C♯3–G♯4 → E3–B4); fixed by sending the tenor
to G♯3 and holding the pedal so E2 stays the real bass. A slur left open at m. 45 was closed.
The tempo map was retuned from 6:13 to 5:52.

*Engraving*: temporary D-minor key signature for mm. 33–36; system and page breaks at phrase
ends, with page turns at rests (mm. 16, 44, 72); caesura glyph; duplicate rests replaced by
spacers; una corda moved off the pedal line.

## 6. Final quality gate (adversarial)

| Category | Score | Evidence |
|---|---|---|
| Melodic identity & development | 8/10 | Distinctive rhythm (pickup / long ♭6 / short / long fall). Audible in every section (mm. 2, 17–21, 33, 41, 61, 73). S is a real counter-gesture, and its sigh fuses with M. Against: wave 1 repeats one rhythm for four bars, and S is less memorable than M. |
| Harmonic sophistication & coherence | 8/10 | Ger+6 with G♮/F𝄪 respelling (11–12); chromatic-mediant dominant chain (18–20); diminished-seventh ascent with spelling chosen by resolution (37–40); deceptive harmony sounding over the dominant pedal one bar early (49); soprano/bass exchange of A and G♯ (50–51); reprise changed by single semitones (C♯→C♮, B♯→B). Against: the applied-dominant chain in wave 2 is textbook, and mm. 33–34 sit on a static D pedal. |
| Dramatic architecture & climax | 8/10 | Peaks mf (21) < f (31) < ff (40) < fff (50–51). Register widens to C♯7 (49) and A0 (51). Each wave falls back partway. The texture comes apart in two bars (52–53). Against: ff runs from m. 40 to m. 49, so the climax's dynamic contrast depends on fff only at 50–51. |
| Pianistic playability & notation | 8/10 | Validated: no same-hand span over an octave, no more than 5 notes per hand, no hand overlap, no leap over 2 octaves inside 0.35 s, 0 LilyPond warnings, page turns at rests. Against: four bars of right-hand four-note chords on every beat (46–49) at stringendo are tiring, and the bass–chord leaps in mm. 30 and 44–45 are demanding. |
| Emotional authenticity & ending | 9/10 | The reprise is the same melody with the floor taken away. The silent cadence (67) and the contracted S (70) give A′ its emptiness. The last sound is a sigh into a hollow fifth, with the missing E as the point. Against: the long rests in mm. 75–77 need a performer who can hold a hall's attention. |

**Weakest section: wave 2 (mm. 25–28).** Its two-bar units (motif over an applied dominant,
then S over the resolution) repeated in identical rhythm, in bare octaves. **Revision made:**
m. 27 now states the motif in its original pickup rhythm, with a sustained inner C♯5 (the
seventh of D♯7) that resolves to B4 on the downbeat of m. 28. m. 28's S is extended to four
rising steps (G♯–A♯–B–C♯–D♯), so the second unit is audibly more urgent than the first.
After the change, music.ly, music.mxl and music.midi were rebuilt and every validation check
was re-run; all pass (see `validation_report.txt`).
