"""MIDI performance render from the canonical event model.

Tempo map: per-measure tempo segments (with ritardandi as ramps) plus fermata
holds; velocities follow the notated dynamics and hairpins with voicing of the
melody; damper / una corda pedals follow the notated pedalling."""
from fractions import Fraction as F
import mido

TPQ = 480
LEVEL = {"ppp": 22, "pp": 31, "p": 42, "mp": 54, "mf": 66, "f": 80, "ff": 96, "fff": 112,
         "sf": 100, "sfz": 104, "fp": 80}
FERMATA_STRETCH = 1.8


def _abs(m, t):
    return (m.num - 1) * 4 + float(t * 4)          # in quarter notes


def tempo_points(measures):
    """Return sorted [(quarter_time, bpm)] step points (ramps discretised)."""
    pts, cur = [], 56.0
    for m in measures:
        segs = m.tempo or [(0, 4, cur, cur)]
        for b0, b1, v0, v1 in segs:
            steps = max(1, int((b1 - b0) * 4))
            for i in range(steps):
                t = b0 + (b1 - b0) * i / steps
                v = v0 + (v1 - v0) * (i + 0.5) / steps if v0 != v1 else v0
                pts.append(((m.num - 1) * 4 + t, float(v)))
            cur = v1
    # fermata holds: stretch every fermata event's span
    holds = []
    for m in measures:
        for vid in ("RA", "RB", "LA", "LB", "MK", "DYN"):
            for ev in m.events[vid] or []:
                if ev.fermata:
                    holds.append((_abs(m, ev.onset), _abs(m, ev.onset + ev.dur)))
    pts.sort()

    def bpm_at(t):
        b = pts[0][1]
        for pt, v in pts:
            if pt <= t + 1e-9:
                b = v
            else:
                break
        return b

    cuts = sorted({p[0] for p in pts} | {h[0] for h in holds} | {h[1] for h in holds})
    out = []
    for c in cuts:
        b = bpm_at(c)
        if any(h0 <= c + 1e-9 < h1 for h0, h1 in holds):
            b /= FERMATA_STRETCH
        if not out or abs(out[-1][1] - b) > 1e-6:
            out.append((c, b))
    return out


def dynamic_curve(measures):
    """Velocity level over score time (quarters): step changes at dynamics,
    linear ramps across hairpins (to the next dynamic, or +/-10 at a \\!)."""
    marks = []
    for m in measures:
        for ev in m.events["DYN"] or []:
            t = _abs(m, ev.onset)
            for h in ev.hairpins:
                if h == "!":
                    marks.append((t, 0, "end", None))
            for d in ev.dynamics:
                marks.append((t, 1, "dyn", d))
            for h in ev.hairpins:
                if h in "<>":
                    marks.append((t, 2, "hp", h))
    marks.sort(key=lambda x: (x[0], x[1]))
    segs = []          # (t0, t1, v0, v1)
    level, t_last = LEVEL["pp"], 0.0
    open_hp = None
    for t, _, kind, val in marks:
        if kind == "dyn":
            new = LEVEL[val]
            if open_hp:
                segs.append((open_hp[0], t, open_hp[1], new))
                open_hp = None
            else:
                segs.append((t_last, t, level, level))
            level, t_last = new, t
        elif kind == "hp":
            if open_hp:   # chained hairpins: close previous at +/-10
                tgt = open_hp[1] + (10 if open_hp[2] == "<" else -10)
                segs.append((open_hp[0], t, open_hp[1], tgt))
                level = tgt
            else:
                segs.append((t_last, t, level, level))
            open_hp = (t, level, val)
            t_last = t
        elif kind == "end" and open_hp:
            tgt = open_hp[1] + (10 if open_hp[2] == "<" else -10)
            segs.append((open_hp[0], t, open_hp[1], tgt))
            level, t_last, open_hp = tgt, t, None
    segs.append((t_last, 1e9, level, level))

    def at(t):
        for a, b, v0, v1 in segs:
            if a <= t < b:
                return v0 + (v1 - v0) * ((t - a) / (b - a)) if b > a else v1
        return level
    return at


def render(measures, path):
    tpts = tempo_points(measures)
    vel_at = dynamic_curve(measures)
    mid = mido.MidiFile(type=1, ticks_per_beat=TPQ)
    t0 = mido.MidiTrack(); mid.tracks.append(t0)
    t0.append(mido.MetaMessage("track_name", name="An Unfinished Grief", time=0))
    t0.append(mido.MetaMessage("time_signature", numerator=4, denominator=4, time=0))
    t0.append(mido.MetaMessage("key_signature", key="C#m", time=0))
    tempo_msgs = [(int(round(t * TPQ)), mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(b)))
                  for t, b in tpts]
    tracks = {}
    for hand, name in (("RH", "Right hand"), ("LH", "Left hand")):
        tr = mido.MidiTrack(); mid.tracks.append(tr)
        tr.append(mido.MetaMessage("track_name", name=name, time=0))
        tracks[hand] = []
    tracks["RH"].append((0, 0, mido.Message("program_change", program=0, channel=0)))
    # notes (merge ties)
    notes = []   # (hand, start_q, end_q, midi, vel)
    for vid, hand in (("RA", "RH"), ("RB", "RH"), ("LA", "LH"), ("LB", "LH")):
        open_ties = {}
        for m in measures:
            for ev in m.events[vid] or []:
                if ev.kind != "note":
                    continue
                st, en = _abs(m, ev.onset), _abs(m, ev.onset + ev.dur)
                if "staccato" in ev.artics:
                    en = st + (en - st) * 0.5
                ps = sorted(ev.pitches, key=lambda p: p.midi)
                new_open = {}
                for i, p in enumerate(ps):
                    if p.midi in open_ties:
                        n = open_ties.pop(p.midi)
                        n[2] = en
                        if ev.tie:
                            new_open[p.midi] = n
                        continue
                    v = vel_at(st)
                    if vid == "RA":
                        v += 9 if i == len(ps) - 1 else -3
                    elif vid == "RB":
                        v -= 7
                    else:
                        v += 2 if i == 0 else -6
                    if "accent" in ev.artics:
                        v += 12
                    if "marcato" in ev.artics:
                        v += 16
                    if "tenuto" in ev.artics:
                        v += 4
                    n = [hand, st, en, p.midi, max(14, min(124, int(round(v))))]
                    notes.append(n)
                    if ev.tie:
                        new_open[p.midi] = n
                open_ties.update(new_open)
    # resolve same-pitch overlaps (two voices striking one key)
    notes.sort(key=lambda n: (n[3], n[1]))
    for a, b in zip(notes, notes[1:]):
        if a[3] == b[3] and a[2] > b[1]:
            a[2] = max(a[1] + 0.05, b[1] - 0.01)
    for hand, st, en, p, v in notes:
        tracks[hand].append((int(round(st * TPQ)), 1, mido.Message("note_on", note=p, velocity=v, channel=0)))
        tracks[hand].append((int(round(en * TPQ)) - 2, 0, mido.Message("note_off", note=p, velocity=0, channel=0)))
    # pedals (on the LH track, same channel)
    for m in measures:
        for ev in m.events["PED"] or []:
            tk = int(round(_abs(m, ev.onset) * TPQ))
            if "sustainOff" in ev.pedals:
                tracks["LH"].append((max(0, tk - 12), 0, mido.Message("control_change", control=64, value=0, channel=0)))
            if "sustainOn" in ev.pedals:
                tracks["LH"].append((tk + 24, 2, mido.Message("control_change", control=64, value=110, channel=0)))
        for vid in ("DYN", "PED"):
            for ev in m.events[vid] or []:
                tk = int(round(_abs(m, ev.onset) * TPQ))
                for _, txt in ev.texts:
                    if txt == "una corda":
                        tracks["LH"].append((tk, 0, mido.Message("control_change", control=67, value=127, channel=0)))
                    if txt == "tre corde":
                        tracks["LH"].append((tk, 0, mido.Message("control_change", control=67, value=0, channel=0)))
    last = max(n[2] for n in notes)
    end_tick = int(round((len(measures) * 4) * TPQ))
    tracks["LH"].append((end_tick, 0, mido.Message("control_change", control=64, value=0, channel=0)))

    def emit(track, items):
        items.sort(key=lambda x: (x[0], x[1]))
        now = 0
        for tk, _, msg in items:
            track.append(msg.copy(time=tk - now))
            now = tk
        return now

    emit(t0, [(tk, 0, msg) for tk, msg in tempo_msgs])
    t0.append(mido.MetaMessage("end_of_track", time=end_tick - tempo_msgs[-1][0]))
    for i, hand in enumerate(("RH", "LH")):
        now = emit(mid.tracks[i + 1], tracks[hand])
        mid.tracks[i + 1].append(mido.MetaMessage("end_of_track", time=max(0, end_tick - now)))
    mid.save(path)
    return mid
