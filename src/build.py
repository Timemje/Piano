"""Assemble the score from section files and export all formats."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from notation import build
import emit_ly, emit_xml, emit_midi

def load():
    from sec_a import SECTION_A
    data = list(SECTION_A)
    for mod, name in (("sec_b", "SECTION_B"), ("sec_c", "SECTION_C"), ("sec_d", "SECTION_D")):
        try:
            data += getattr(__import__(mod), name)
        except ModuleNotFoundError:
            pass
    return build(data)

if __name__ == "__main__":
    measures, errors = load()
    for e in errors:
        print("ERROR:", e)
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    with open(os.path.join(out, "music.ly"), "w") as f:
        f.write(emit_ly.render(measures))
    xml = emit_xml.render(measures)
    emit_xml.write_mxl(xml, os.path.join(out, "music.mxl"))
    mid = emit_midi.render(measures, os.path.join(out, "music.midi"))
    print(f"MIDI length {mid.length:.1f} s")
    print(f"{len(measures)} measures, {len(errors)} errors")
