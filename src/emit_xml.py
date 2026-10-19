"""MusicXML exporter: writes a compressed .mxl directly from the event model."""
from fractions import Fraction as F
from math import lcm
import zipfile
from xml.sax.saxutils import escape

from notation import STAFF

VOICE_NO = {"RA": 1, "RB": 2, "LA": 5, "LB": 6}
TYPE = {1: "whole", 2: "half", 4: "quarter", 8: "eighth", 16: "16th", 32: "32nd"}
KEY_FIFTHS = {("c", "major"): 0, ("g", "major"): 1, ("d", "major"): 2, ("a", "major"): 3,
              ("e", "major"): 4, ("f", "major"): -1, ("bes", "major"): -2, ("ees", "major"): -3,
              ("a", "minor"): 0, ("e", "minor"): 1, ("b", "minor"): 2, ("fis", "minor"): 3,
              ("cis", "minor"): 4, ("d", "minor"): -1, ("g", "minor"): -2, ("c", "minor"): -3}


def key_alters(fifths):
    order = "FCGDAEB" if fifths > 0 else "BEADGCF"
    return {s: (1 if fifths > 0 else -1) for s in order[:abs(fifths)]}


KEY_ALTER = key_alters(4)
ACC_NAME = {0: "natural", 1: "sharp", -1: "flat", 2: "double-sharp", -2: "flat-flat"}
DYN_SOUND = {"ppp": 25, "pp": 36, "p": 50, "mp": 64, "mf": 78, "f": 92, "ff": 106, "fff": 120,
             "sf": 100, "sfz": 105, "fp": 90}
ARTIC_XML = {"accent": "accent", "staccato": "staccato", "tenuto": "tenuto",
             "marcato": "strong-accent", "portato": "detached-legato",
             "staccatissimo": "staccatissimo"}


def _divisions(measures):
    d = 1
    for m in measures:
        for v, evs in m.events.items():
            for ev in evs or []:
                d = lcm(d, (ev.dur * 4).denominator, (ev.onset * 4).denominator)
    return d


class XW:
    def __init__(self):
        self.lines = []

    def add(self, s):
        self.lines.append(s)


def _dur(fr, div):
    q = fr * 4 * div
    assert q.denominator == 1, fr
    return int(q)


def _directions(m, div, w):
    """Dynamics, hairpins, pedals, texts and tempo marks as <direction>s.
    Emitted after all voices, positioned with <forward> from the measure start."""
    items = []
    for vid, staff, place in (("MK", 1, "above"), ("DYN", 1, "below"), ("PED", 2, "below")):
        for ev in m.events[vid] or []:
            t = ev.onset
            if ev.tempo:
                items.append((t, 0, staff, "above", ("tempo", ev.tempo)))
            for d, txt in ev.texts:
                items.append((t, 1, staff, "above" if d == "up" else "below", ("words", txt)))
            for dn in ev.dynamics:
                items.append((t, 2, staff, place, ("dyn", dn)))
            for h in ev.hairpins:
                items.append((t, 1 if h == "!" else 3, staff, place, ("wedge", h)))
            peds = list(ev.pedals)
            if "sustainOff" in peds and "sustainOn" in peds:
                items.append((t, 4, staff, place, ("pedal", "change")))
            elif "sustainOn" in peds:
                items.append((t, 4, staff, place, ("pedal", "start")))
            elif "sustainOff" in peds:
                items.append((t, 4, staff, place, ("pedal", "stop")))
    items.sort(key=lambda x: (x[0], x[1]))
    cur = F(0)
    for t, _, staff, place, (kind, val) in items:
        if t > cur:
            w.add(f"<forward><duration>{_dur(t - cur, div)}</duration></forward>")
            cur = t
        if kind == "pedal":
            dt = f'<pedal type="{val}" line="yes" sign="{"yes" if val == "start" else "no"}"/>'
        elif kind == "dyn":
            dt = f"<dynamics><{val}/></dynamics>"
        elif kind == "wedge":
            typ = {"<": "crescendo", ">": "diminuendo", "!": "stop"}[val]
            dt = f'<wedge type="{typ}" number="1"/>'
        elif kind == "words":
            dt = f'<words font-style="italic">{escape(val)}</words>'
        elif kind == "tempo":
            text, unit, bpm = val
            dt = ""
            if text:
                dt += f'<words font-weight="bold">{escape(text)}</words>'
            if bpm:
                if dt:
                    dt += "</direction-type><direction-type>"
                dt += f"<metronome><beat-unit>quarter</beat-unit><per-minute>{bpm}</per-minute></metronome>"
        sound = ""
        if kind == "dyn":
            sound = f'<sound dynamics="{DYN_SOUND[val]}"/>'
        if kind == "tempo" and val[2]:
            sound = f'<sound tempo="{val[2]}"/>'
        if kind == "pedal":
            sound = {"start": '<sound damper-pedal="yes"/>', "stop": '<sound damper-pedal="no"/>'}.get(val, "")
        w.add(f'<direction placement="{place}"><direction-type>{dt}</direction-type>'
              f"<staff>{staff}</staff>{sound}</direction>")
    return cur


def tempo_changes(measures):
    """Essential tempo changes shared with the MIDI tempo map: (measure, bpm)
    at each bar whose opening tempo differs from the previous bar's end."""
    out, cur = [], None
    for m in measures:
        segs = m.tempo
        if segs:
            v0 = segs[0][2]
            if cur is None or abs(v0 - cur) >= 1:
                out.append((m.num, v0))
            cur = segs[-1][3]
    return out


def render(measures, title="An Unfinished Grief"):
    div = _divisions(measures)
    w = XW()
    w.add('<?xml version="1.0" encoding="UTF-8" standalone="no"?>')
    w.add('<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 4.0 Partwise//EN" '
          '"http://www.musicxml.org/dtds/partwise.dtd">')
    w.add('<score-partwise version="4.0">')
    w.add(f"<work><work-title>{escape(title)}</work-title></work>")
    w.add("<movement-title>An Unfinished Grief — Concert Prelude for Solo Piano</movement-title>")
    w.add("<identification><encoding><software>canonical event model (src/emit_xml.py)</software>"
          "</encoding></identification>")
    w.add('<part-list><score-part id="P1"><part-name>Piano</part-name>'
          '<score-instrument id="P1-I1"><instrument-name>Piano</instrument-name></score-instrument>'
          '<midi-instrument id="P1-I1"><midi-channel>1</midi-channel><midi-program>1</midi-program>'
          "</midi-instrument></score-part></part-list>")
    w.add('<part id="P1">')
    tie_open = {v: {} for v in VOICE_NO}      # voice -> {pitch key: True}
    slur_stack = {v: [] for v in VOICE_NO}
    ottava_on = {1: False, 2: False}
    tchg = dict(tempo_changes(measures))
    KEY_ALTER = key_alters(4)
    for idx, m in enumerate(measures):
        w.add(f'<measure number="{m.num}">')
        if idx == 0:
            w.add(f"<attributes><divisions>{div}</divisions><key><fifths>4</fifths><mode>minor</mode></key>"
                  "<time><beats>4</beats><beat-type>4</beat-type></time><staves>2</staves>"
                  '<clef number="1"><sign>G</sign><line>2</line></clef>'
                  '<clef number="2"><sign>F</sign><line>4</line></clef></attributes>')
        if m.num in tchg:
            w.add(f'<sound tempo="{tchg[m.num]:g}"/>')
        kc = next((ev.key for ev in (m.events["RA"] or []) if ev.key), None)
        if kc:
            fifths = KEY_FIFTHS[kc]
            KEY_ALTER = key_alters(fifths)
            w.add(f"<attributes><key><fifths>{fifths}</fifths><mode>{kc[1]}</mode></key></attributes>")
        acc_state = {1: {}, 2: {}}
        first_voice = True
        for vid in ("RA", "RB", "LA", "LB"):
            evs = m.events[vid]
            if evs is None:
                continue
            if not first_voice:
                w.add(f"<backup><duration>{_dur(F(1), div)}</duration></backup>")
            first_voice = False
            staff = STAFF[vid]
            other = {"RA": "RB", "RB": "RA", "LA": "LB", "LB": "LA"}[vid]
            poly = m.events[other] is not None
            stem = ("up" if vid in ("RA", "LA") else "down") if poly else None
            vno = VOICE_NO[vid]
            for ev in evs:
                if ev.clef:
                    sign, line = ("G", 2) if ev.clef == "treble" else ("F", 4)
                    w.add(f'<attributes><clef number="{staff}"><sign>{sign}</sign><line>{line}</line></clef></attributes>')
                if ev.ottava is not None:
                    if ev.ottava == 0 and ottava_on[staff]:
                        w.add(f'<direction><direction-type><octave-shift type="stop" size="8" number="1"/>'
                              f"</direction-type><staff>{staff}</staff></direction>")
                        ottava_on[staff] = False
                    elif ev.ottava != 0:
                        typ = "down" if ev.ottava > 0 else "up"
                        w.add(f'<direction placement="{"above" if ev.ottava > 0 else "below"}"><direction-type>'
                              f'<octave-shift type="{typ}" size="8" number="1"/></direction-type>'
                              f"<staff>{staff}</staff></direction>")
                        ottava_on[staff] = True
                d = _dur(ev.dur, div)
                if ev.kind == "space":
                    w.add(f"<forward><duration>{d}</duration><voice>{vno}</voice><staff>{staff}</staff></forward>")
                    continue
                base, dots = ev.written
                typ = TYPE[base]
                tm = ""
                if ev.tuplet:
                    tm = (f"<time-modification><actual-notes>{ev.tuplet[0]}</actual-notes>"
                          f"<normal-notes>{ev.tuplet[1]}</normal-notes></time-modification>")
                if ev.kind == "rest":
                    whole = ev.dur == 1 and len(evs) == 1
                    nots = "<notations><fermata/></notations>" if ev.fermata else ""
                    w.add(f'<note><rest{" measure=\"yes\"" if whole else ""}/><duration>{d}</duration>'
                          f"<voice>{vno}</voice>{'' if whole else f'<type>{typ}</type>' + '<dot/>' * dots}"
                          f"{tm}<staff>{staff}</staff>{nots}</note>")
                    continue
                ordered = sorted(ev.pitches, key=lambda p: p.midi)
                for i, p in enumerate(ordered):
                    k = p.key()
                    tie_stop = tie_open[vid].pop(k, False)
                    tie_start = ev.tie
                    acc = ""
                    if not tie_stop:
                        st = acc_state[staff].get((p.step, p.octave), KEY_ALTER.get(p.step, 0))
                        if st != p.alter:
                            acc = f"<accidental>{ACC_NAME[p.alter]}</accidental>"
                        acc_state[staff][(p.step, p.octave)] = p.alter
                    ties = ""
                    tied = ""
                    if tie_stop:
                        ties += '<tie type="stop"/>'
                        tied += '<tied type="stop"/>'
                    if tie_start:
                        ties += '<tie type="start"/>'
                        tied += '<tied type="start"/>'
                        tie_open[vid][k] = True
                    nots = tied
                    if i == 0:
                        for _ in range(ev.slur_stop):
                            if slur_stack[vid]:
                                nots += f'<slur type="stop" number="{slur_stack[vid].pop()}"/>'
                        for _ in range(ev.slur_start):
                            n = 1
                            while n in slur_stack[vid]:
                                n += 1
                            slur_stack[vid].append(n)
                            nots += f'<slur type="start" number="{n}"/>'
                        if ev.tuplet and ev.tuplet[2] in ("start", "single"):
                            nots += '<tuplet type="start" bracket="no"/>'
                        if ev.tuplet and ev.tuplet[2] in ("stop", "single"):
                            nots += '<tuplet type="stop"/>'
                        arts = "".join(f"<{ARTIC_XML[a]}/>" for a in ev.artics)
                        if arts:
                            nots += f"<articulations>{arts}</articulations>"
                        if ev.fermata:
                            nots += "<fermata/>"
                        if ev.fingers:
                            nots += "<technical>" + "".join(f"<fingering>{x}</fingering>" for x in ev.fingers) + "</technical>"
                    nots = f"<notations>{nots}</notations>" if nots else ""
                    alter = f"<alter>{p.alter}</alter>" if p.alter else ""
                    w.add(f"<note>{'<chord/>' if i else ''}<pitch><step>{p.step}</step>{alter}"
                          f"<octave>{p.octave}</octave></pitch><duration>{d}</duration>{ties}"
                          f"<voice>{vno}</voice><type>{typ}</type>{'<dot/>' * dots}{acc}{tm}"
                          f"{f'<stem>{stem}</stem>' if stem else ''}<staff>{staff}</staff>{nots}</note>")
        w.add(f"<backup><duration>{_dur(F(1), div)}</duration></backup>")
        cur = _directions(m, div, w)
        if cur < 1:
            w.add(f"<forward><duration>{_dur(1 - cur, div)}</duration></forward>")
        if idx == len(measures) - 1:
            w.add('<barline location="right"><bar-style>light-heavy</bar-style></barline>')
        elif m.src["MK"] and '\\bar "||"' in m.src["MK"]:
            w.add('<barline location="right"><bar-style>light-light</bar-style></barline>')
        w.add("</measure>")
    w.add("</part></score-partwise>")
    return "\n".join(w.lines)


def write_mxl(xml_text, path, inner="music.musicxml"):
    container = ('<?xml version="1.0" encoding="UTF-8"?>\n<container><rootfiles>'
                 f'<rootfile full-path="{inner}" media-type="application/vnd.recordare.musicxml+xml"/>'
                 "</rootfiles></container>")
    with zipfile.ZipFile(path, "w") as z:
        z.writestr(zipfile.ZipInfo("mimetype"), "application/vnd.recordare.musicxml",
                   compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml", container, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr(inner, xml_text, compress_type=zipfile.ZIP_DEFLATED)
