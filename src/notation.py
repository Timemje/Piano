"""Canonical note-event model for 'An Unfinished Grief'.

The score is written as a strict subset of LilyPond syntax (absolute pitch),
one string per voice per measure.  This module parses those strings into a
timed event model that every exporter (LilyPond, MusicXML, MIDI) and the
validator share.
"""
from fractions import Fraction as F
import re

STEPS = "CDEFGAB"
SEMI = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
ALTER = {"": 0, "is": 1, "es": -1, "isis": 2, "eses": -2}
DYNAMICS = ("ppp", "pp", "p", "mp", "mf", "f", "ff", "fff", "sfz", "sf", "fp")
MEASURE_LEN = F(1)  # 4/4, in whole notes

TOKEN_RE = re.compile(r"""
  (?P<tuplet>\\tuplet\s+(?P<tn>\d+)/(?P<td>\d+)\s*\{)
 |(?P<tclose>\})
 |(?P<tempo>\\tempo\s+(?:"(?P<ttext>[^"]*)")?\s*(?:(?P<tunit>\d+)\s*=\s*(?P<tbpm>\d+))?)
 |(?P<barline>\\bar\s+"[^"]*")
 |(?P<key>\\key\s+(?P<ktonic>[a-g](?:is|es)?)\s+\\(?P<kmode>major|minor))
 |(?P<clef>\\clef\s+"?(?P<clefname>treble|bass)"?)
 |(?P<ottava>\\ottava\s+\#(?P<ott>-?\d))
 |(?P<text>(?P<tdir>[\^_-])"(?P<tstr>[^"]*)")
 |(?P<phr>\\[()])
 |(?P<hairpin>\\[<>!])
 |(?P<dyn>\\(?P<dname>ppp|pp|p|mp|mf|fff|ff|f|sfz|sf|fp)(?![A-Za-z]))
 |(?P<pedal>\\(?P<pname>sustainOn|sustainOff|unaCorda|treCorde))
 |(?P<fermata>\\fermata)
 |(?P<cmd>\\[A-Za-z]+)
 |(?P<artic>-(?P<aname>[>.\-^_!]))
 |(?P<finger>-(?P<fnum>[1-5]))
 |(?P<chopen><)
 |(?P<chclose>>)
 |(?P<rest>(?P<rkind>[rsR])(?![a-z]))
 |(?P<note>(?P<nname>[a-g])(?P<nacc>isis|eses|is|es)?(?P<noct>[',]*))
 |(?P<dur>(?P<dval>16|32|1|2|4|8)(?P<ddots>\.*))
 |(?P<tie>~)
 |(?P<slur>[()])
 |(?P<bar>\|)
 |(?P<ws>\s+)
""", re.X)

ARTIC_NAMES = {">": "accent", ".": "staccato", "-": "tenuto", "^": "marcato",
               "_": "portato", "!": "staccatissimo"}


class Pitch:
    __slots__ = ("step", "alter", "octave")

    def __init__(self, step, alter, octave):
        self.step, self.alter, self.octave = step, alter, octave

    @property
    def midi(self):
        return 12 * (self.octave + 1) + SEMI[self.step] + self.alter

    def name(self):
        acc = {0: "", 1: "#", -1: "b", 2: "x", -2: "bb"}[self.alter]
        return f"{self.step}{acc}{self.octave}"

    def key(self):
        return (self.step, self.alter, self.octave)


def parse_pitch(name, acc, octs):
    octave = 3 + octs.count("'") - octs.count(",")
    return Pitch(name.upper(), ALTER[acc or ""], octave)


class Event:
    """One rhythmic slot in one voice: a note, chord, rest or spacer."""

    def __init__(self, kind, pitches, dur, written, onset):
        self.kind = kind            # 'note' | 'rest' | 'space'
        self.pitches = pitches      # list[Pitch]
        self.dur = dur              # Fraction of a whole note (actual)
        self.written = written      # (base, dots) e.g. (8, 1)
        self.onset = onset          # Fraction, relative to measure start
        self.tie = False            # tie to next event of this voice
        self.slur_start = 0
        self.slur_stop = 0
        self.phr_start = 0
        self.phr_stop = 0
        self.artics = []
        self.fingers = []
        self.fermata = False
        self.dynamics = []          # names
        self.hairpins = []          # '<', '>', '!'
        self.pedals = []            # sustainOn/sustainOff/unaCorda/treCorde
        self.texts = []             # (dir, text)
        self.tempo = None           # (text, unit, bpm)
        self.clef = None
        self.key = None             # (tonic, mode) key change at this event
        self.ottava = None
        self.tuplet = None          # (actual, normal, 'start'|'mid'|'stop'|'single')
        self.measure = None
        self.voice = None


class ParseError(Exception):
    pass


class VoiceParser:
    """Keeps LilyPond's duration carry-over state for one persistent voice."""

    def __init__(self, vid):
        self.vid = vid
        self.last = (4, 0)

    def parse(self, src, mnum):
        events, t = [], F(0)
        pending = {}
        factor = [F(1)]
        tuplet_stack = []
        in_chord, chord = False, []
        last_ev = None
        first_dur_seen = False
        pos = 0
        expect_dur_for = None  # ('note', pitches) / ('rest', kind) / ('chord', pitches)

        def finish(item, dur_tok):
            nonlocal t, last_ev, first_dur_seen
            if dur_tok is None:
                if not first_dur_seen:
                    raise ParseError(f"m{mnum} {self.vid}: first event needs explicit duration: {src!r}")
                base, dots = self.last
            else:
                base, dots = dur_tok
                self.last = dur_tok
                first_dur_seen = True
            d = F(1, base)
            add = d
            for _ in range(dots):
                add /= 2
                d += add
            d *= factor[-1]
            kind, pitches = item
            ev = Event(kind, pitches, d, (base, dots), t)
            ev.measure, ev.voice = mnum, self.vid
            for k, v in pending.items():
                setattr(ev, k, v)
            pending.clear()
            if tuplet_stack:
                tup = tuplet_stack[-1]
                tup["events"].append(ev)
            events.append(ev)
            t += d
            last_ev = ev

        while pos < len(src):
            m = TOKEN_RE.match(src, pos)
            if not m:
                raise ParseError(f"m{mnum} {self.vid}: cannot parse at {src[pos:pos+20]!r}")
            pos = m.end()
            g = m.lastgroup
            if g == "ws" or g == "bar":
                continue
            # A pending note/rest/chord waiting for an optional duration
            if expect_dur_for is not None:
                if g == "dur":
                    finish(expect_dur_for, (int(m["dval"]), len(m["ddots"])))
                    expect_dur_for = None
                    continue
                finish(expect_dur_for, None)
                expect_dur_for = None
            if in_chord:
                if g == "note":
                    chord.append(parse_pitch(m["nname"], m["nacc"], m["noct"]))
                elif g == "chclose":
                    in_chord = False
                    expect_dur_for = ("note", chord)
                else:
                    raise ParseError(f"m{mnum} {self.vid}: unexpected {m.group()!r} in chord")
                continue
            if g == "note":
                expect_dur_for = ("note", [parse_pitch(m["nname"], m["nacc"], m["noct"])])
            elif g == "rest":
                expect_dur_for = ({"r": "rest", "R": "rest", "s": "space"}[m["rkind"]], [])
            elif g == "chopen":
                in_chord, chord = True, []
            elif g == "dur":
                raise ParseError(f"m{mnum} {self.vid}: stray duration {m.group()!r}")
            elif g == "tuplet":
                fac = F(int(m["td"]), int(m["tn"]))
                factor.append(factor[-1] * fac)
                tuplet_stack.append({"n": int(m["tn"]), "d": int(m["td"]), "events": []})
            elif g == "tclose":
                factor.pop()
                tup = tuplet_stack.pop()
                evs = tup["events"]
                for i, ev in enumerate(evs):
                    role = "single" if len(evs) == 1 else ("start" if i == 0 else "stop" if i == len(evs) - 1 else "mid")
                    ev.tuplet = (tup["n"], tup["d"], role)
            elif g == "tempo":
                pending["tempo"] = (m["ttext"], int(m["tunit"]) if m["tunit"] else None,
                                    int(m["tbpm"]) if m["tbpm"] else None)
            elif g == "key":
                pending["key"] = (m["ktonic"], m["kmode"])
            elif g == "clef":
                pending["clef"] = m["clefname"]
            elif g == "ottava":
                pending["ottava"] = int(m["ott"])
            elif g == "barline":
                pass  # layout-only
            elif g == "cmd":
                pass  # layout-only passthrough (e.g. \stemUp); kept verbatim in .ly
            else:
                # postfix attachments to the previous event
                if last_ev is None:
                    raise ParseError(f"m{mnum} {self.vid}: postfix {m.group()!r} without event")
                ev = last_ev
                if g == "tie":
                    ev.tie = True
                elif g == "slur":
                    if m.group() == "(":
                        ev.slur_start += 1
                    else:
                        ev.slur_stop += 1
                elif g == "phr":
                    if m.group() == "\\(":
                        ev.phr_start += 1
                    else:
                        ev.phr_stop += 1
                elif g == "artic":
                    ev.artics.append(ARTIC_NAMES[m["aname"]])
                elif g == "finger":
                    ev.fingers.append(int(m["fnum"]))
                elif g == "fermata":
                    ev.fermata = True
                elif g == "dyn":
                    ev.dynamics.append(m["dname"])
                elif g == "hairpin":
                    ev.hairpins.append(m.group()[1])
                elif g == "pedal":
                    ev.pedals.append(m["pname"])
                elif g == "text":
                    ev.texts.append(({"^": "up", "_": "down", "-": "down"}[m["tdir"]], m["tstr"]))
                else:
                    raise ParseError(f"m{mnum} {self.vid}: unhandled {g}")
        if expect_dur_for is not None:
            finish(expect_dur_for, None)
        if in_chord or tuplet_stack:
            raise ParseError(f"m{mnum} {self.vid}: unterminated chord/tuplet")
        return events, t


VOICES = ("RA", "RB", "LA", "LB", "DYN", "PED", "MK")
HAND = {"RA": "RH", "RB": "RH", "LA": "LH", "LB": "LH"}
STAFF = {"RA": 1, "RB": 1, "LA": 2, "LB": 2}


class Measure:
    def __init__(self, num, src, events, tempo, harm):
        self.num = num
        self.src = src          # vid -> source string or None
        self.events = events    # vid -> list[Event] (None if voice inactive)
        self.tempo = tempo      # MIDI tempo segments [(beat0, beat1, bpm0, bpm1)]
        self.harm = harm


def M(num, ra=None, rb=None, la=None, lb=None, dyn=None, ped=None, mk=None,
      tempo=None, harm=""):
    return dict(num=num, RA=ra, RB=rb, LA=la, LB=lb, DYN=dyn, PED=ped, MK=mk,
                tempo=tempo, harm=harm)


def build(measure_dicts):
    parsers = {v: VoiceParser(v) for v in VOICES}
    measures, errors = [], []
    for d in measure_dicts:
        n = d["num"]
        src, evs = {}, {}
        for v in VOICES:
            s = d[v]
            src[v] = s
            if s is None:
                evs[v] = None
                continue
            try:
                e, total = parsers[v].parse(s, n)
            except ParseError as ex:
                errors.append(str(ex))
                evs[v] = None
                continue
            if total != MEASURE_LEN:
                errors.append(f"m{n} {v}: duration {total} != 1 ({s!r})")
            evs[v] = e
        measures.append(Measure(n, src, evs, d["tempo"], d["harm"]))
    nums = [m.num for m in measures]
    if nums != list(range(1, len(nums) + 1)):
        errors.append(f"measure numbering not contiguous: {nums}")
    return measures, errors


def note_events(measures, hands=("RA", "RB", "LA", "LB")):
    """Yield (measure, vid, event) for every sounding note/chord event."""
    for m in measures:
        for v in hands:
            for ev in m.events[v] or []:
                if ev.kind == "note":
                    yield m, v, ev
