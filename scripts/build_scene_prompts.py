#!/usr/bin/env python3
"""Expand one episode's authored scene records into both prompt files.

One source (the SC lines in scenes.txt) drives the image prompt file and the video
prompt file, so the 1 to 1 between breakdown lines, image prompts and video prompts is
true by construction rather than by hand.

Usage:
    python3 build_scene_prompts.py <episode_dir> [--register documentary|animation]
                                   [--wpm R] [--refs tail|inline] [--out DIR]
                                   [--no-footer]

Reads:
    <episode_dir>/scenes.txt             N records, 11 fields separated by " ~ "
    <episode_dir>/characters.txt         "N. NAME" lines, for the footer
    <episode_dir>/scene_breakdown.txt    narration beats, read by line number

Writes:
    <out>/movie_scene_prompts.txt        image prompts, [NAME] anchors
    <out>/animation_scene_prompts.txt    video prompts, @NAME anchors

Notes:
    records are read from scenes.txt and every scenes-NN.txt beside it, in numeric
    order, so a long episode can be authored in chunks.
    --refs tail appends ", using [NAME] from the uploaded references" to the place
    clause; --refs inline expects the anchor to already appear inside the place text.
"""
import argparse
import glob
import os
import re
import sys

REGISTERS = {
    "documentary": {
        "image": ("Rendered as an ultra photorealistic historical documentary frame, cinematic "
                  "realism, practical lighting, authentic textures, muted earth-tone color palette, "
                  "subtle Kodak Vision3 film look, soft natural contrast, fine organic film grain, "
                  "high dynamic range without artificial HDR, historically accurate materials and "
                  "costumes, shallow depth of field only where physically appropriate, 35mm "
                  "cinematic lens, 16:9, no text, no logos, no captions."),
        "video": ("Photorealistic historical documentary style, practical available light, authentic "
                  "weathered textures, muted earth tone palette, fine organic film grain, no gloss, "
                  "no digital sheen."),
        "refs_mode": "tail",
    },
    "animation": {
        "image": "Rendered in clean cinematic stylized Pixar animation style, highly detailed.",
        "video": ("Soft pixar animation style, smooth surfaces, subtle imperfections, practical "
                  "studio lighting, shallow depth of field, tactile animated film aesthetic."),
        "refs_mode": "inline",
    },
}

KEEP = "Keep the exact design from the uploaded references."
AUDIO = "No dialogue, no music, no subtitles, no new objects."
FIELDS = ["n", "label", "flag", "refs", "place", "use", "emotion", "action",
          "movement", "background", "camera"]


def load_identities(episode):
    path = os.path.join(episode, "characters.txt")
    if not os.path.exists(path):
        raise SystemExit(f"missing {path}")
    names = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            m = re.match(r"^\d+\.\s*([A-Z][A-Z0-9 \-]+)$", line.strip())
            if m:
                names.append(m.group(1).strip())
    if not names:
        raise SystemExit(f"no 'N. NAME' lines parsed from {path}")
    if len(names) > 6:
        raise SystemExit(f"cast cap is six, characters.txt declares {len(names)}")
    return names


def load_scenes(episode):
    paths = sorted(glob.glob(os.path.join(episode, "scenes*.txt")))
    if not paths:
        raise SystemExit(f"no scenes*.txt under {episode}")
    scenes = []
    for path in paths:
        with open(path, encoding="utf-8") as f:
            for lineno, line in enumerate(f, 1):
                line = line.rstrip("\n").strip()
                if not line or line.startswith("#"):
                    continue
                f_ = [x.strip() for x in line.split(" ~ ")]
                if len(f_) != 11:
                    raise SystemExit(
                        f"{os.path.basename(path)}:{lineno} has {len(f_)} fields, not 11. "
                        f"An empty refs field is written as two spaces between the tildes.")
                if not f_[0].startswith("SC"):
                    raise SystemExit(f"{os.path.basename(path)}:{lineno} bad scene id {f_[0]!r}")
                s = dict(zip(FIELDS, f_))
                s["n"] = int(s["n"][2:])
                if s["flag"] not in ("ANIMATE", "HOLD"):
                    raise SystemExit(f"scene {s['n']}: flag {s['flag']!r} is not ANIMATE or HOLD")
                scenes.append(s)
    scenes.sort(key=lambda s: s["n"])
    got = [s["n"] for s in scenes]
    if got != list(range(1, len(scenes) + 1)):
        raise SystemExit(f"scene numbers are not sequential 1..N: {got[:20]}")
    return scenes


def load_beats(episode):
    path = os.path.join(episode, "scene_breakdown.txt")
    if not os.path.exists(path):
        raise SystemExit(f"missing {path}. Run chunk_scenes.py first.")
    out = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            m = re.match(r"^\d+\.\s*(.*)$", line)
            if not m:
                raise SystemExit(f"scene_breakdown.txt line is not numbered: {line[:60]!r}")
            out.append(m.group(1).strip())
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("episode")
    ap.add_argument("--register", choices=sorted(REGISTERS), default="documentary")
    ap.add_argument("--wpm", type=float, default=None)
    ap.add_argument("--refs", choices=["tail", "inline", "auto"], default="auto")
    ap.add_argument("--out", default=None)
    ap.add_argument("--no-footer", action="store_true", dest="no_footer")
    args = ap.parse_args()

    reg = REGISTERS[args.register]
    refs_mode = reg["refs_mode"] if args.refs == "auto" else args.refs
    out_dir = args.out or args.episode
    os.makedirs(out_dir, exist_ok=True)

    identities = load_identities(args.episode)
    scenes = load_scenes(args.episode)
    beats = load_beats(args.episode)

    n = len(scenes)
    if len(beats) != n:
        raise SystemExit(
            f"{len(beats)} breakdown lines vs {n} scene records. The chunker is "
            f"authoritative for the scene count: re-read the line count it printed and "
            f"author exactly that many records. The builder asserts rather than padding.")

    movie, animation = [], []
    for s in scenes:
        beat = beats[s["n"] - 1]
        refs = [r.strip() for r in s["refs"].split(",") if r.strip()]
        for r in refs:
            if r not in identities:
                raise SystemExit(f"scene {s['n']}: ref {r!r} is not declared in characters.txt")

        place = s["place"]
        if refs:
            if refs_mode == "tail":
                place = (place + ", using " + ", ".join(f"[{r}]" for r in refs)
                         + " from the uploaded references")
            else:
                missing = [r for r in refs if f"[{r}]" not in place]
                if missing:
                    raise SystemExit(
                        f"scene {s['n']}: refs mode is inline but {missing} do not appear "
                        f"in the place clause")

        movie.append(f"SCENE {s['n']}\nPlace {place}\n{KEEP}\nUse {s['use']}\n{reg['image']}")

        scene_line = s["label"] or s["place"][:60]
        if refs:
            scene_line = scene_line + ", " + " ".join(f"@{r}" for r in refs)
        animation.append(
            f"SCENE {s['n']}\nScene: {scene_line}\nEmotion: {s['emotion']}\n"
            f"Action: {s['action']}\nMovement: {s['movement']}\n"
            f"Background: {s['background']}\nCamera: {s['camera']}\n"
            f"Style: {reg['video']}")

    footer = ""
    if not args.no_footer:
        footer = "\n\n---\nANCHOR TAGS\n" + "\n".join(f"[{x}] = @" for x in identities) + "\n"

    with open(os.path.join(out_dir, "movie_scene_prompts.txt"), "w", encoding="utf-8") as f:
        f.write("\n\n".join(movie) + footer)
    with open(os.path.join(out_dir, "animation_scene_prompts.txt"), "w", encoding="utf-8") as f:
        f.write("\n\n".join(animation) + footer)

    # Prove the anchors survived the wrap.
    for fname, pattern in (("movie_scene_prompts.txt", r"\[([A-Z][A-Z0-9 \-]+)\]"),
                           ("animation_scene_prompts.txt", r"@([A-Z][A-Z0-9 \-]+)")):
        body = open(os.path.join(out_dir, fname), encoding="utf-8").read()
        found = {r.strip() for r in re.findall(pattern, body)}
        bad = sorted(r for r in found if r not in identities)
        if bad:
            raise SystemExit(f"{fname}: refs not declared in characters.txt: {bad}")

    anim = sum(1 for s in scenes if s["flag"] == "ANIMATE")
    print(f"{os.path.basename(os.path.normpath(args.episode))}: scenes {n} | "
          f"ANIMATE {anim} ({anim / n * 100:.0f} percent) | HOLD {n - anim}")
    print(f"identities {len(identities)}: {', '.join(identities)}")
    print(f"register {args.register} | refs {refs_mode} | footer {'omitted' if args.no_footer else 'written'}")
    print(f"wrote {out_dir}/movie_scene_prompts.txt and {out_dir}/animation_scene_prompts.txt")


if __name__ == "__main__":
    sys.exit(main())
