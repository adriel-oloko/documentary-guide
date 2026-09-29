#!/usr/bin/env python3
"""The gate. Run this on an episode folder, fix what it flags, run it again.

Usage:
    python3 verify_documentary.py <episode_dir> [<episode_dir> ...]
    python3 verify_documentary.py <parent_of_episodes>
    python3 verify_documentary.py <episode_dir> --wpm 151.4 --lane long --strict

Point it at an episode folder, or at a folder whose children are episode folders, and
it walks them. Exit status is 1 if anything FAILED.

Hard checks, all FAIL:
    file presence (the nine house files)
    breakdown concatenation reproduces script.txt word for word
    tag parity and tag inventory on script-tagged.txt
    breakdown line count, and the scene count in each prompt file
    SCENE label order, with lowercase b scenes allowed
    every ref in a body appears in that file's ANCHOR TAGS footer
    every ref is declared in characters.txt
    the two footers are byte identical
    cast ceiling of six, and characters.txt and character_prompts.txt agreeing
    scenes.txt record shape, numbering and refs, when scenes.txt exists
    the exact style line present once per scene in each prompt file
    copy rules on every file

Advisory checks, WARN unless --strict:
    the script word band for the lane
    the clip length band derived from scene_timings.txt
    digits surviving in narration (years and figures should be words)
    a declared identity that never appears in a shot
    a voiceover present whose measured duration disagrees with the timing column

A FAIL from a freshly written or freshly edited checker is a hypothesis, not a
finding. Prove it on references/worked-example-long/ and references/worked-example-short/
first: both are real, and both must come back PASS.
"""
import argparse
import os
import re
import subprocess
import sys

REQUIRED = ["script.txt", "script-tagged.txt", "characters.txt", "character_prompts.txt",
            "scene_breakdown.txt", "scene_timings.txt", "movie_scene_prompts.txt",
            "animation_scene_prompts.txt", "post.txt"]
OPTIONAL = ["scenes.txt", "00-research.md", "voice.mp3", ".studio-lane"]

IMAGE_LINES = {
    "documentary": ("Rendered as an ultra photorealistic historical documentary frame, cinematic "
                    "realism, practical lighting, authentic textures, muted earth-tone color palette, "
                    "subtle Kodak Vision3 film look, soft natural contrast, fine organic film grain, "
                    "high dynamic range without artificial HDR, historically accurate materials and "
                    "costumes, shallow depth of field only where physically appropriate, 35mm "
                    "cinematic lens, 16:9, no text, no logos, no captions."),
    "animation": "Rendered in clean cinematic stylized Pixar animation style, highly detailed.",
}
VIDEO_LINES = {
    "documentary": ("Style: Photorealistic historical documentary style, practical available light, "
                    "authentic weathered textures, muted earth tone palette, fine organic film grain, "
                    "no gloss, no digital sheen."),
    "animation": ("Style: Soft pixar animation style, smooth surfaces, subtle imperfections, "
                  "practical studio lighting, shallow depth of field, tactile animated film "
                  "aesthetic."),
}
BANDS = {"long": (1450, 1560), "short": (150, 200)}
CLIP_BAND = {"long": (5.0, 8.0), "short": (4.0, 6.0)}
DEFAULT_WPM = {"long": 145.9, "short": 174.0}

WORDS = re.compile(r"[A-Za-z0-9'\u2019$-]+")


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def word_list(text):
    return WORDS.findall(text)


def tag_strip(text):
    return (text.replace("[pause]", " ").replace("[emphasis]", " "))


def probe_duration(path):
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nw=1:nk=1", path],
            capture_output=True, text=True, timeout=30)
        return float(out.stdout.strip())
    except Exception:
        return None


def verify_episode(d, lane, wpm, n_bscenes, strict):
    fails, warns = [], []

    def fail(msg):
        fails.append(msg)

    def warn(msg):
        warns.append(msg)

    name = os.path.basename(os.path.normpath(d))

    # --- presence ---------------------------------------------------------
    for f in REQUIRED:
        if not os.path.exists(os.path.join(d, f)):
            fail(f"{f}: MISSING")
    if fails:
        # Nothing downstream is meaningful without the file set.
        return name, fails, warns

    script = read(os.path.join(d, "script.txt"))
    tagged = read(os.path.join(d, "script-tagged.txt"))
    chars = read(os.path.join(d, "characters.txt"))
    cprompts = read(os.path.join(d, "character_prompts.txt"))
    breakdown = read(os.path.join(d, "scene_breakdown.txt"))
    timings = read(os.path.join(d, "scene_timings.txt"))
    post = read(os.path.join(d, "post.txt"))
    movie = read(os.path.join(d, "movie_scene_prompts.txt"))
    anim = read(os.path.join(d, "animation_scene_prompts.txt"))

    sw = word_list(script)

    # --- word band --------------------------------------------------------
    lo, hi = BANDS[lane]
    if not (lo <= len(sw) <= hi):
        (fail if strict else warn)(
            f"script.txt: {len(sw)} words, outside the {lane} band {lo} to {hi}")

    # --- breakdown concatenation -----------------------------------------
    bd_words, bd_lines = [], []
    for line in breakdown.splitlines():
        if not line.strip():
            continue
        m = re.match(r"^(\d+)\.\s*(.*)$", line)
        if not m:
            fail(f"scene_breakdown.txt: line is not numbered: {line[:50]!r}")
            continue
        bd_lines.append((int(m.group(1)), m.group(2)))
        bd_words.extend(word_list(m.group(2)))
    if bd_words != sw:
        fail(f"scene_breakdown.txt does not reproduce script.txt word for word "
             f"({len(bd_words)} words vs {len(sw)})")
    nums = [n for n, _ in bd_lines]
    if nums != list(range(1, len(bd_lines) + 1)):
        fail("scene_breakdown.txt: line numbers are not sequential from 1")
    n_bd = len(bd_lines)

    # --- tags -------------------------------------------------------------
    if word_list(tag_strip(tagged)) != sw:
        fail("script-tagged.txt: stripping the tags does not reproduce script.txt")
    tags = set(re.findall(r"\[([^\]\[]+)\]", tagged))
    extra = sorted(t for t in tags if t not in ("pause", "emphasis"))
    if extra:
        fail(f"script-tagged.txt: non house tags present: {extra}")

    # --- timings ----------------------------------------------------------
    secs, tnums = [], []
    for line in timings.splitlines():
        m = re.match(r"^(\d+)\.\s*([0-9.]+)s\s*$", line.strip())
        if m:
            tnums.append(int(m.group(1)))
            secs.append(float(m.group(2)))
        elif line.strip():
            warn(f"scene_timings.txt: unparsed line {line[:40]!r}")
    if len(secs) != n_bd:
        fail(f"scene_timings.txt: {len(secs)} entries vs {n_bd} breakdown lines")
    if tnums and tnums != list(range(1, len(tnums) + 1)):
        fail("scene_timings.txt: numbers are not sequential from 1")
    clip_lo, clip_hi = CLIP_BAND[lane]
    off = [i + 1 for i, s in enumerate(secs) if not (clip_lo - 1.0 <= s <= clip_hi + 0.5)]
    if off:
        warn(f"scene_timings.txt: {len(off)} lines outside the {clip_lo:.0f} to {clip_hi:.0f}s "
             f"clip band (lines {off[:8]}{' ...' if len(off) > 8 else ''})")
    voice = os.path.join(d, "voice.mp3")
    if os.path.exists(voice):
        dur = probe_duration(voice)
        if dur:
            drift = abs(sum(secs) - dur) / dur * 100 if dur else 0
            if drift > 2:
                fail(f"scene_timings.txt sums to {sum(secs):.1f}s but voice.mp3 is {dur:.1f}s "
                     f"({drift:.1f} percent off). Re-derive the timings from the measured duration")
            else:
                warn(f"voice.mp3 measured {dur:.1f}s, implied rate "
                     f"{len(sw) / (dur / 60):.1f} wpm")
    elif sum(secs):
        implied = len(sw) / (sum(secs) / 60)
        if not (110 <= implied <= 240):
            warn(f"scene_timings.txt implies {implied:.1f} wpm, outside any plausible "
                 f"narration rate. Check the timing column")
        elif abs(sum(secs) - len(sw) / wpm * 60) / sum(secs) > 0.03:
            warn(f"scene_timings.txt sums to {sum(secs):.1f}s, an implied {implied:.1f} wpm, "
                 f"against the {wpm:.1f} wpm in use. Correct if the column was retimed after "
                 f"a voiceover, otherwise re-derive it at the rate you are actually using")


    # --- cast -------------------------------------------------------------
    char_names = [c.strip() for c in re.findall(r"^\d+\.\s*([A-Z][A-Z0-9 \-]+)$", chars, re.M)]
    if not char_names:
        fail("characters.txt: no 'N. NAME' entries parsed")
    if len(char_names) > 6:
        fail(f"characters.txt: {len(char_names)} identities, cast ceiling is six")
    cp_names = [m.strip() for m in re.findall(r"^([A-Z][A-Z0-9 \-]+)$", cprompts, re.M)]
    if char_names != cp_names:
        fail(f"characters.txt and character_prompts.txt disagree on cast or order: "
             f"{char_names} vs {cp_names}")
    heading_bold = cprompts.count("**")
    if heading_bold != len(char_names) * 2:
        warn(f"character_prompts.txt: {heading_bold} bold markers, expected "
             f"{len(char_names) * 2} (two per identity heading)")

    # --- prompt files -----------------------------------------------------
    expected = n_bd + n_bscenes
    registers = set()
    for fname, content, style, pattern in (
            ("movie_scene_prompts.txt", movie, IMAGE_LINES, "bracket"),
            ("animation_scene_prompts.txt", anim, VIDEO_LINES, "at")):
        labels = re.findall(r"^SCENE (\d+)(b?)$", content, re.M)
        if len(labels) != expected:
            fail(f"{fname}: {len(labels)} SCENE labels vs {n_bd} breakdown lines "
                 f"plus {n_bscenes} b scenes = {expected}")
        order = [(int(a), 1 if b else 0) for a, b in labels]
        if order != sorted(order):
            fail(f"{fname}: SCENE labels are out of order")
        if re.search(r"^SCENE \d+B$", content, re.M):
            fail(f"{fname}: uppercase B scene label (must be lowercase)")
        if "ANCHOR TAGS" not in content or "\n---\n" not in content:
            fail(f"{fname}: missing the --- / ANCHOR TAGS footer")
        body = content.split("ANCHOR TAGS", 1)[0]
        anchors = {a.strip() for a in re.findall(r"^\[([A-Z0-9 \-]+)\] = @$", content, re.M)}
        if pattern == "bracket":
            refs = {r.strip() for r in re.findall(r"\[([A-Z][A-Z0-9 \-]+)\]", body)}
        else:
            refs = {r.strip() for r in re.findall(r"@([A-Z][A-Z0-9 \-]+)", body)}
        for r in sorted(refs - anchors):
            fail(f"{fname}: ref {r} is used but missing from ANCHOR TAGS")
        for r in sorted(refs - set(char_names)):
            fail(f"{fname}: ref {r} is not declared in characters.txt")
        # exact style line, once per scene
        hit = [k for k, v in style.items() if v in content]
        if not hit:
            fail(f"{fname}: the style line for neither register is present. "
                 f"A dropped or paraphrased style line is the most common failure there is")
        else:
            registers.add(hit[0])
            cnt = content.count(style[hit[0]])
            if cnt != len(labels):
                fail(f"{fname}: the {hit[0]} style line appears {cnt} times for "
                     f"{len(labels)} scenes")
        if fname == "movie_scene_prompts.txt":
            movie_footer = content.split("ANCHOR TAGS", 1)[1] if "ANCHOR TAGS" in content else ""
            movie_refs = refs
        else:
            anim_footer = content.split("ANCHOR TAGS", 1)[1] if "ANCHOR TAGS" in content else ""
            anim_refs = refs
    if "ANCHOR TAGS" in movie and "ANCHOR TAGS" in anim:
        if movie_footer != anim_footer:
            fail("the two ANCHOR TAGS footers are not byte identical")
    if len(registers) > 1:
        fail(f"the two prompt files use different registers: {sorted(registers)}")
    used = movie_refs | anim_refs
    for c in char_names:
        if c not in used:
            warn(f"characters.txt declares {c} but no shot references it")

    # --- scene records ----------------------------------------------------
    scenes_path = os.path.join(d, "scenes.txt")
    if os.path.exists(scenes_path):
        recs = {}
        for line in read(scenes_path).splitlines():
            if not line.strip() or line.strip().startswith("#"):
                continue
            f_ = [x.strip() for x in line.split(" ~ ")]
            if len(f_) != 11:
                fail(f"scenes.txt: a record has {len(f_)} fields, not 11 "
                     f"(empty refs is two spaces between the tildes): {line[:50]!r}")
                continue
            if not f_[0].startswith("SC"):
                fail(f"scenes.txt: bad scene id {f_[0]!r}")
                continue
            recs[int(f_[0][2:])] = f_
        if list(sorted(recs)) != list(range(1, len(recs) + 1)):
            fail("scenes.txt: SC numbers are not sequential from 1")
        if len(recs) != n_bd:
            fail(f"scenes.txt: {len(recs)} records vs {n_bd} breakdown lines")
        for n, f_ in sorted(recs.items()):
            for r in [x.strip() for x in f_[3].split(",") if x.strip()]:
                if r not in char_names:
                    fail(f"scenes.txt scene {n}: ref {r} not declared in characters.txt")
            if f_[2] not in ("ANIMATE", "HOLD"):
                fail(f"scenes.txt scene {n}: flag {f_[2]!r}")
    else:
        warn("scenes.txt absent, so the scene records could not be checked "
             "(fine for a hand-authored prompt set, required if you used the builder)")

    # --- digits in narration ---------------------------------------------
    digits = re.findall(r"\b\d[\d,.]*\b", script)
    if digits:
        warn(f"script.txt: {len(digits)} digit tokens in narration, years and figures "
             f"should be words (first few: {digits[:5]})")

    # --- copy rules -------------------------------------------------------
    for f in REQUIRED + (["scenes.txt"] if os.path.exists(scenes_path) else []):
        t = read(os.path.join(d, f))
        bad = {}
        if re.search(r"[\u2014\u2013]", t):
            bad["dash"] = len(re.findall(r"[\u2014\u2013]", t))
        if re.search(r'["\u201c\u201d\u2018\u2019]', t):
            bad["quote"] = len(re.findall(r'["\u201c\u201d\u2018\u2019]', t))
        if "?" in t:
            bad["qmark"] = t.count("?")
        if re.search(r"\b(you|your|yours)\b", t, re.I):
            bad["second person"] = len(re.findall(r"\b(you|your|yours)\b", t, re.I))
        if "**" in t and f != "character_prompts.txt":
            bad["bold"] = t.count("**")
        if bad:
            fail(f"{f}: copy rules violated: {bad}")

    return name, fails, warns


def infer_lane(episode):
    """SHORT below 400 script words, LONG above. Only used when --lane is not given."""
    path = os.path.join(episode, "script.txt")
    if not os.path.exists(path):
        return "long"
    return "short" if len(word_list(read(path))) <= 400 else "long"


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--lane", choices=["auto", "long", "short"], default="auto",
                    help="default auto: SHORT below 400 script words, LONG above")
    ap.add_argument("--wpm", type=float, default=None)
    ap.add_argument("--bscenes", type=int, default=0)
    ap.add_argument("--strict", action="store_true",
                    help="promote advisory checks to failures")
    args = ap.parse_args()

    targets = []
    for p in args.paths:
        if os.path.exists(os.path.join(p, "script.txt")):
            targets.append(p)
        else:
            for entry in sorted(os.listdir(p)):
                sub = os.path.join(p, entry)
                if os.path.isdir(sub) and os.path.exists(os.path.join(sub, "script.txt")):
                    targets.append(sub)
    if not targets:
        print("no episode folders found. An episode folder contains script.txt.")
        return 2

    failed = False
    n_fail = n_warn = 0
    for d in targets:
        lane = infer_lane(d) if args.lane == "auto" else args.lane
        wpm = args.wpm if args.wpm is not None else DEFAULT_WPM[lane]
        name, fails, warns = verify_episode(d, lane, wpm, args.bscenes, args.strict)
        if fails:
            failed = True
            n_fail += len(fails)
            print(f"FAIL {name}  [{lane}]")
            for m in fails:
                print(f"  - {m}")
        else:
            print(f"OK   {name}  [{lane}]")
        for m in warns:
            n_warn += 1
            print(f"  ~ {m}")

    print(f"\n{len(targets)} episode(s) | {n_fail} failure(s) | {n_warn} advisory note(s)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
