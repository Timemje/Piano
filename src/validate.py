"""Programmatic validation of the score and all exported files.

Usage: python3 src/validate.py [out_dir] [work_dir]
Writes validation_report.txt into out_dir.  Every number in the report is
measured here; nothing is assumed."""
import os, sys, subprocess, zipfile, io, re, datetime
from fractions import Fraction as F
from collections import defaultdict
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(__file__))
from build import load
from notation import HAND, SEMI
import emit_ly

OUT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
WORK = os.path.abspath(sys.argv[2] if len(sys.argv) > 2 else os.path.join(OUT, "build_check"))
os.makedirs(WORK, exist_ok=True)
report, failures = [], []


def line(s=""):
    report.append(s)


def check(ok, label, detail=""):
    line(f"  [{'PASS' if ok else 'FAIL'}] {label}" + (f" — {detail}" if detail else ""))
    if not ok:
        failures.append(label)


measures, parse_errors = load()
NUM = len(measures)

# ---------------------------------------------------------------- model notes
def model_notes():
    """Every notated note head: (hand, abs_onset_whole, midi, (step,alter,oct), dur, vid, measure)."""
    out = []
    for m in measures:
        for vid in ("RA", "RB", "LA", "LB"):
            for ev in m.events[vid] or []:
                if ev.kind == "note":
                    for p in ev.pitches:
                        out.append((HAND[vid], (m.num - 1) + ev.onset, p.midi, p.key(), ev.dur, vid, m.num))
    return out


def sustained_intervals():
    """Ties merged into single sustained notes: per hand list of (start, end, midi, measure)."""
    res = defaultdict(list)
    for vid in ("RA", "RB", "LA", "LB"):
        open_t = {}
        for m in measures:
            for ev in m.events[vid] or []:
                if ev.kind != "note":
                    open_t = {}
                    continue
                st, en = (m.num - 1) + ev.onset, (m.num - 1) + ev.onset + ev.dur
                nxt = {}
                for p in ev.pitches:
                    if p.midi in open_t:
                        rec = open_t.pop(p.midi)
                        rec[1] = en
                    else:
                        rec = [st, en, p.midi, m.num]
                        res[HAND[vid]].append(rec)
                    if ev.tie:
                        nxt[p.midi] = rec
                open_t = nxt
    return res


MN = model_notes()
SUS = sustained_intervals()

line("VALIDATION REPORT — An Unfinished Grief (Concert Prelude for Solo Piano)")
line(f"Generated {datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} by src/validate.py")
line(f"Canonical model: {NUM} measures, {len(MN)} notated note heads "
     f"(RH {sum(1 for n in MN if n[0]=='RH')}, LH {sum(1 for n in MN if n[0]=='LH')}).")
line()

# ---------------------------------------------------------------- 1 & 2 spans
line("1. CHORD-SPAN VALIDATION (same hand, all simultaneously sounding notated notes,")
line("   tied/sustained voices merged, checked at every onset boundary)")
worst = {}
viol_span, viol_count = [], []
for hand, ivs in SUS.items():
    bounds = sorted({iv[0] for iv in ivs})
    w = (0, None)
    for t in bounds:
        act = [iv for iv in ivs if iv[0] <= t < iv[1]]
        ps = sorted({iv[2] for iv in act})
        span = ps[-1] - ps[0]
        mnum = int(t) + 1
        beat = float((t - int(t)) * 4) + 1
        if span > w[0]:
            w = (span, (mnum, beat, ps))
        if span > 12:
            viol_span.append((hand, mnum, beat, ps, span))
        if len(ps) > 5:
            viol_count.append((hand, mnum, beat, ps))
    worst[hand] = w
for hand in ("RH", "LH"):
    s, (mnum, beat, ps) = worst[hand]
    line(f"  {hand}: widest simultaneous span = {s} semitones (m. {mnum}, beat {beat:g}, MIDI {ps})")
check(not viol_span, "no same-hand span exceeds 12 semitones",
      f"{len(viol_span)} violations" + ("" if not viol_span else ": " + "; ".join(
          f"{h} m.{m} b{b:g} {ps} ({s})" for h, m, b, ps, s in viol_span[:10])))
line()
line("2. SIMULTANEOUS NOTE-COUNT VALIDATION")
maxc = {}
for hand, ivs in SUS.items():
    best = (0, None)
    for t in sorted({iv[0] for iv in ivs}):
        c = len({iv[2] for iv in ivs if iv[0] <= t < iv[1]})
        if c > best[0]:
            best = (c, int(t) + 1)
    maxc[hand] = best
    line(f"  {hand}: maximum simultaneous notes = {best[0]} (first at m. {best[1]})")
check(not viol_count, "no hand ever holds more than five notes", f"{len(viol_count)} violations")
line()

# ---------------------------------------------------------------- 3 durations
line("3. MEASURE-DURATION VALIDATION (4/4; each voice summed independently,")
line("   tuplets scaled, spacer rests counted, voices not double-counted)")
bad = []
voices_checked = 0
for m in measures:
    for vid in ("RA", "RB", "LA", "LB", "DYN", "PED", "MK"):
        evs = m.events[vid]
        if evs is None:
            continue
        voices_checked += 1
        tot = sum((e.dur for e in evs), F(0))
        if tot != 1:
            bad.append((m.num, vid, tot))
check(not parse_errors, "source parses without errors", "; ".join(parse_errors[:5]))
check(not bad, f"all {voices_checked} active voice-measures total exactly one 4/4 bar",
      "; ".join(f"m{a} {b}={c}" for a, b, c in bad[:10]))
contig = [m.num for m in measures] == list(range(1, NUM + 1))
check(contig, f"measures numbered contiguously 1–{NUM}, no repeats, no pickup")
line()

# ---------------------------------------------------------------- 4 files
line("4. FILE INTEGRITY")
ly_path = os.path.join(OUT, "music.ly")
pdf_path = os.path.join(OUT, "music.pdf")
mid_path = os.path.join(OUT, "music.midi")
mxl_path = os.path.join(OUT, "music.mxl")
r = subprocess.run(["lilypond", "-o", os.path.join(WORK, "music_recompile"), ly_path],
                   capture_output=True, text=True, cwd=WORK)
warns = [l for l in r.stderr.splitlines() if "warning" in l.lower() or "error" in l.lower()]
check(r.returncode == 0, "LilyPond compilation of music.ly exits successfully",
      f"exit code {r.returncode}; {len(warns)} warnings/errors in log")
for wl in warns[:10]:
    line(f"      log: {wl}")
lyver = subprocess.run(["lilypond", "--version"], capture_output=True, text=True).stdout.splitlines()[0]
line(f"      ({lyver})")
pi = subprocess.run(["pdfinfo", pdf_path], capture_output=True, text=True)
pages = re.search(r"Pages:\s+(\d+)", pi.stdout)
check(pi.returncode == 0 and pages is not None, "music.pdf is a readable PDF",
      f"{pages.group(1) if pages else '?'} pages, {os.path.getsize(pdf_path)} bytes")
pt = subprocess.run(["pdftotext", pdf_path, "-"], capture_output=True, text=True)
check("An Unfinished Grief" in pt.stdout, "PDF text layer contains the title")
import mido
try:
    mf = mido.MidiFile(mid_path)
    nmid = sum(1 for tr in mf.tracks for msg in tr if msg.type == "note_on" and msg.velocity > 0)
    check(True, "music.midi parses with mido",
          f"type {mf.type}, {len(mf.tracks)} tracks, {mf.ticks_per_beat} TPQ, {nmid} note-ons")
except Exception as ex:
    mf = None
    check(False, "music.midi parses with mido", str(ex))
try:
    z = zipfile.ZipFile(mxl_path)
    names = z.namelist()
    mt = z.read("mimetype").decode() if "mimetype" in names else ""
    cont = ET.fromstring(z.read("META-INF/container.xml"))
    root_path = cont.find(".//rootfile").get("full-path")
    xml_bytes = z.read(root_path)
    xroot = ET.fromstring(xml_bytes)
    ok = (names[0] == "mimetype" and mt == "application/vnd.recordare.musicxml"
          and z.getinfo("mimetype").compress_type == zipfile.ZIP_STORED and xroot.tag == "score-partwise")
    check(ok, "music.mxl is a valid compressed MusicXML package",
          f"entries {names}; rootfile {root_path}; root <{xroot.tag} version={xroot.get('version')}>")
except Exception as ex:
    xml_bytes = None
    check(False, "music.mxl is a valid compressed MusicXML package", str(ex))
import music21
try:
    sc = music21.converter.parse(mxl_path)
    parts = list(sc.parts)
    check(len(parts) == 2, "MusicXML reopens in music21 without parsing errors",
          f"music21 {music21.__version__}: {len(parts)} staves, "
          f"{len(parts[0].getElementsByClass('Measure'))} measures")
except Exception as ex:
    sc = None
    check(False, "MusicXML reopens in music21 without parsing errors", str(ex))
line()

# ---------------------------------------------------------------- 5 cross-format
line("5. CROSS-FORMAT CONSISTENCY against the canonical event model")
model_set = defaultdict(list)
for hand, t, midi, key, dur, vid, mnum in MN:
    model_set[hand].append((t, key, dur))

import mido
# 5a LilyPond's own interpretation of music.ly (event-listener dump)
chk = os.path.join(WORK, "check.ly")
with open(chk, "w") as f:
    f.write(emit_ly.render(measures, hook=True))
ev_file = os.path.join(WORK, "lily_events.tsv")
if os.path.exists(ev_file):
    os.remove(ev_file)
r2 = subprocess.run(["lilypond", "-s", "-dno-print-pages", "-o", os.path.join(WORK, "check"), chk],
                    capture_output=True, text=True, cwd=WORK)
ly_notes = defaultdict(list)
ly_rests = defaultdict(int)
if os.path.exists(ev_file):
    for row in open(ev_file):
        kind, staff, voice, mom, nn, alt, octv, dur = row.rstrip("\n").split("\t")
        hand = "RH" if staff == "up" else "LH"
        if kind == "note":
            alt = F(alt)
            key = (STEPS_ := "CDEFGAB")[int(nn)], int(alt * 2), int(octv) + 4
            ly_notes[hand].append((F(mom), key, F(dur)))
        else:
            ly_rests[hand] += 1


def compare(a, b):
    sa, sb = sorted(a), sorted(b)
    if sa == sb:
        return True, ""
    from collections import Counter
    ca, cb = Counter(sa), Counter(sb)
    miss, extra = list((ca - cb).elements()), list((cb - ca).elements())
    return False, f"missing {len(miss)} e.g. {miss[:3]}; extra {len(extra)} e.g. {extra[:3]}"


# LilyPond's own MIDI rendering of the check build (one track per staff)
ly_mid_path = os.path.join(WORK, "check.midi")
ly_midi_notes = defaultdict(list)
if os.path.exists(ly_mid_path):
    lm = mido.MidiFile(ly_mid_path)
    note_tracks = [tr for tr in lm.tracks if any(m.type == "note_on" for m in tr)]
    for hand, tr in zip(("RH", "LH"), note_tracks):
        now = 0
        for msg in tr:
            now += msg.time
            if msg.type == "note_on" and msg.velocity > 0:
                ly_midi_notes[hand].append((F(now, lm.ticks_per_beat * 4), msg.note))

model_rests = defaultdict(int)
for m in measures:
    for vid in ("RA", "RB", "LA", "LB"):
        for ev in m.events[vid] or []:
            if ev.kind == "rest" and m.src[vid].strip() != "R1":
                model_rests[HAND[vid]] += 1
for hand in ("RH", "LH"):
    ok, why = compare(model_set[hand], ly_notes[hand])
    check(ok and r2.returncode == 0, f"LilyPond ({hand}): pitches+spelling, onsets, durations match model",
          f"{len(ly_notes[hand])} LilyPond note events vs {len(model_set[hand])} model" + (f"; {why}" if why else ""))
    check(ly_rests[hand] == model_rests[hand], f"LilyPond ({hand}): rest count matches model",
          f"{ly_rests[hand]} vs {model_rests[hand]}")

for hand in ("RH", "LH"):
    exp = [(F(iv[0]).limit_denominator(1920), iv[2]) for iv in SUS[hand]]
    ok, why = compare(exp, ly_midi_notes[hand])
    check(ok, f"LilyPond-generated MIDI ({hand}): sustained notes match model",
          f"{len(ly_midi_notes[hand])} vs {len(exp)}" + (f"; {why}" if why else ""))

# 5b MusicXML re-read by music21
if sc is not None:
    xml_notes = defaultdict(list)
    for si, part in enumerate(sc.parts):
        hand = "RH" if si == 0 else "LH"
        for meas in part.getElementsByClass("Measure"):
            base = F(meas.number - 1)
            for n in meas.recurse().notes:
                off = F(n.getOffsetInHierarchy(meas)).limit_denominator(96) / 4
                dur = F(n.duration.quarterLength).limit_denominator(96) / 4
                pitches = n.pitches
                for p in pitches:
                    alter = int(p.accidental.alter) if p.accidental else 0
                    xml_notes[hand].append((base + off, (p.step, alter, p.octave), dur))
    for hand in ("RH", "LH"):
        ok, why = compare(model_set[hand], xml_notes[hand])
        check(ok, f"MusicXML ({hand}): pitches+spelling, onsets, durations, staff match model",
              f"{len(xml_notes[hand])} vs {len(model_set[hand])}" + (f"; {why}" if why else ""))
    import emit_xml
    mm_model = [(m.num, ev.tempo[0]) for m in measures for ev in (m.events["MK"] or []) if ev.tempo]
    if xml_bytes:
        xr0 = ET.fromstring(xml_bytes)
        words_x = [(int(me.get("number")), w.text) for me in xr0.iter("measure")
                   for w in me.iter("words") if w.get("font-weight") == "bold"]
        check([(a, b) for a, b in mm_model if b] == words_x,
              "MusicXML: tempo texts at the same measures as the model",
              f"{len(words_x)} tempo texts: " + ", ".join(f"m{a} {b}" for a, b in words_x))
        snd_x = [(int(me.get("number")), float(sd.get("tempo"))) for me in xr0.iter("measure")
                 for sd in me.findall("sound") if sd.get("tempo")]
        exp = [(a, float(b)) for a, b in emit_xml.tempo_changes(measures)]

        def midi_bpm(mnum):
            tk, t, bpm = (mnum - 1) * 4 * mf.ticks_per_beat, 0, None
            for msg in mf.tracks[0]:
                t += msg.time
                if msg.type == "set_tempo" and t <= tk:
                    bpm = mido.tempo2bpm(msg.tempo)
            return bpm
        diffs = [(a, b, round(midi_bpm(a), 2)) for a, b in exp if abs(midi_bpm(a) - b) > 1.0] if mf else exp
        check(snd_x == exp and not diffs,
              "essential tempo changes agree: model, MusicXML <sound tempo>, MIDI tempo map",
              f"{len(snd_x)} changes, e.g. " + ", ".join(f"m{a}={b:g}" for a, b in snd_x[:10])
              + (f"; MIDI differs at {diffs[:5]}" if diffs else ""))
    dyn_model = sum(len(ev.dynamics) for m in measures for ev in (m.events["DYN"] or []))
    dyn_xml = len(list(sc.recurse().getElementsByClass(music21.dynamics.Dynamic)))
    check(dyn_model == dyn_xml, "MusicXML: dynamic marks preserved", f"{dyn_xml} vs {dyn_model}")
    sl_model = sum(ev.slur_start for m in measures for v in ("RA", "RB", "LA", "LB") for ev in (m.events[v] or []))
    sl_xml = len([s for s in sc.recurse().getElementsByClass(music21.spanner.Slur)])
    check(sl_model == sl_xml, "MusicXML: slurs preserved", f"{sl_xml} vs {sl_model}")
    if xml_bytes:
        xr = ET.fromstring(xml_bytes)
        ped = len(xr.findall(".//pedal"))
        ped_model = sum(1 for m in measures for ev in (m.events["PED"] or [])
                        if "sustainOn" in ev.pedals or "sustainOff" in ev.pedals)
        check(ped == ped_model, "MusicXML: pedal marks preserved", f"{ped} vs {ped_model}")
        ties_x = len(xr.findall(".//tie[@type='start']"))
        ties_m = sum(len(ev.pitches) for m in measures for v in ("RA", "RB", "LA", "LB")
                     for ev in (m.events[v] or []) if ev.tie and ev.kind == "note")
        check(ties_x == ties_m, "MusicXML: ties preserved", f"{ties_x} vs {ties_m}")
        meas_x = len(xr.findall(".//measure"))
        check(meas_x == NUM, "MusicXML: complete repeat-free measure structure",
              f"{meas_x} measures, {len(xr.findall('.//repeat'))} repeats")

# 5c MIDI note content (ties merged) against the model
if mf is not None:
    midi_notes = defaultdict(list)
    for ti, tr in enumerate(mf.tracks[1:3]):
        hand = "RH" if ti == 0 else "LH"
        now, on = 0, {}
        for msg in tr:
            now += msg.time
            if msg.type == "note_on" and msg.velocity > 0:
                on[msg.note] = now
            elif msg.type in ("note_off", "note_on") and msg.note in on:
                st = on.pop(msg.note)
                midi_notes[hand].append((F(st, mf.ticks_per_beat * 4), msg.note))
    for hand in ("RH", "LH"):
        exp = [(F(iv[0]).limit_denominator(1920), iv[2]) for iv in SUS[hand]]
        ok, why = compare(exp, midi_notes[hand])
        check(ok, f"MIDI ({hand}): every sustained note (ties merged) present with correct pitch and onset",
              f"{len(midi_notes[hand])} vs {len(exp)}" + (f"; {why}" if why else ""))
line()

# ---------------------------------------------------------------- 6 duration
line("6. PERFORMANCE DURATION (from the MIDI tempo map, incl. ritardandi and fermatas)")
if mf is not None:
    secs = mf.length
    tempos = [mido.tempo2bpm(m.tempo) for tr in mf.tracks for m in tr if m.type == "set_tempo"]
    line(f"  MIDI length: {secs:.1f} s = {int(secs // 60)}:{secs % 60:04.1f}")
    line(f"  tempo map: {len(tempos)} tempo events, range {min(tempos):.1f}–{max(tempos):.1f} BPM (quarter)")
    sect = [("A  (1–16)", 1, 16), ("B  (17–40)", 17, 40), ("C  (41–56)", 41, 56),
            ("A' (57–72)", 57, 72), ("Coda (73–80)", 73, 80)]
    # seconds per section from the tempo map
    tick = 0
    tmap = []
    for msg in mf.tracks[0]:
        tick += msg.time
        if msg.type == "set_tempo":
            tmap.append((tick, msg.tempo))

    def sec_at(tk):
        s, last_t, last_tempo = 0.0, 0, tmap[0][1]
        for t, tp in tmap:
            if t >= tk:
                break
            s += (t - last_t) / mf.ticks_per_beat * last_tempo / 1e6
            last_t, last_tempo = t, tp
        return s + (tk - last_t) / mf.ticks_per_beat * last_tempo / 1e6
    for name, a, b in sect:
        s0, s1 = sec_at((a - 1) * 4 * mf.ticks_per_beat), sec_at(b * 4 * mf.ticks_per_beat)
        line(f"    {name}: {s1 - s0:6.1f} s")
    check(300 <= secs <= 360, "estimated duration within the 5–6 minute target", f"{secs/60:.2f} min")
line()

# ---------------------------------------------------------------- extra checks
line("7. ADDITIONAL MUSICAL / NOTATIONAL CHECKS")
allp = [n[2] for n in MN]
check(min(allp) >= 21 and max(allp) <= 108, "all pitches inside the piano range A0–C8",
      f"lowest MIDI {min(allp)}, highest MIDI {max(allp)}")
# hand crossing at simultaneous onsets
cross = []
for t in sorted({iv[0] for iv in SUS['RH']} | {iv[0] for iv in SUS['LH']}):
    rh = [iv[2] for iv in SUS["RH"] if iv[0] <= t < iv[1]]
    lh = [iv[2] for iv in SUS["LH"] if iv[0] <= t < iv[1]]
    if rh and lh and max(lh) > min(rh):
        cross.append((int(t) + 1, float((t - int(t)) * 4) + 1, max(lh), min(rh)))
check(not cross, "no hand crossing / overlapping hand positions (LH top <= RH bottom)",
      f"{len(cross)} instances" + (": " + str(cross[:6]) if cross else ""))
# pedal syntax
state, ped_err = False, []
for m in measures:
    for ev in m.events["PED"] or []:
        p = ev.pedals
        if "sustainOff" in p and not state:
            ped_err.append(f"m{m.num}: release while up")
        if "sustainOff" in p:
            state = False
        if "sustainOn" in p:
            if state:
                ped_err.append(f"m{m.num}: depress while down")
            state = True
check(not ped_err and not state, "pedal depressions and releases alternate correctly; pedal up at the end",
      "; ".join(ped_err[:5]))
# slur balance
sl_err = []
for vid in ("RA", "RB", "LA", "LB"):
    depth = 0
    for m in measures:
        for ev in m.events[vid] or []:
            depth -= ev.slur_stop
            if depth < 0:
                sl_err.append(f"m{m.num} {vid}")
                depth = 0
            depth += ev.slur_start
    if depth:
        sl_err.append(f"{vid} ends with {depth} open slur(s)")
check(not sl_err, "slurs balanced in every voice", "; ".join(sl_err))
# ties connect equal pitches
tie_err = []
for vid in ("RA", "RB", "LA", "LB"):
    prev = None
    for m in measures:
        for ev in m.events[vid] or []:
            if ev.kind == "space":
                continue
            if prev is not None and prev.tie:
                if ev.kind != "note" or not {p.midi for p in prev.pitches} & {p.midi for p in ev.pitches}:
                    tie_err.append(f"m{m.num} {vid}")
            prev = ev
check(not tie_err, "every tie lands on the same pitch in the next event", "; ".join(tie_err[:5]))
# fast leaps within one hand (playability heuristic): > 24 semitones in < 0.35 s
leaps = []
if mf is not None:
    def sec_of(t_whole):
        return sec_at(int(t_whole * 4 * mf.ticks_per_beat))
    for hand in ("RH", "LH"):
        onsets = sorted({iv[0] for iv in SUS[hand]})
        for a, b in zip(onsets, onsets[1:]):
            pa = [iv[2] for iv in SUS[hand] if iv[0] == a]
            pb = [iv[2] for iv in SUS[hand] if iv[0] == b]
            jump = min(abs(x - y) for x in pa for y in pb)
            dt = sec_of(b) - sec_of(a)
            if jump > 24 and dt < 0.35:
                leaps.append((hand, int(b) + 1, jump, round(dt, 2)))
check(not leaps, "no leap over two octaves inside 0.35 s in either hand",
      f"{len(leaps)}" + (f": {leaps[:6]}" if leaps else ""))
line()

line("8. SCORE INSPECTION")
line("  Automated: LilyPond log scanned above for warnings (collisions, bar-check failures, etc.).")
line("  Manual: every PDF page rasterised (pdftoppm, 90–200 dpi) and inspected; findings are")
line("  recorded below (src/inspection_notes.txt).")
notes_file = os.path.join(os.path.dirname(__file__), "inspection_notes.txt")
if os.path.exists(notes_file):
    for l in open(notes_file):
        line("  " + l.rstrip())
line()
line("SUMMARY")
line(f"  {len(failures)} failed checks" + (": " + "; ".join(failures) if failures else " — all checks passed."))
with open(os.path.join(OUT, "validation_report.txt"), "w") as f:
    f.write("\n".join(report) + "\n")
print("\n".join(report))
sys.exit(1 if failures else 0)
