#!/usr/bin/env python3
"""Slice a script into numbered shot lines and per line timings.

Sentences are atomic. A sentence longer than the band splits at the boundary nearest
its middle: a comma, semicolon or colon first, then a conjunction or preposition, then
by force. Short units merge up to the floor, then a capped rebalance pass moves words
between neighbours until every line is in the band.

Usage:
    python3 chunk_scenes.py <script.txt> <out_dir> [--lane long|short] [--wpm R]
                            [--min-sec S] [--max-sec S]
    python3 chunk_scenes.py <out_dir> --retime-only --wpm R

Writes:
    <out_dir>/scene_breakdown.txt    "N. <script text>"
    <out_dir>/scene_timings.txt      "N. X.XXs"

The words across the lines always equal the script word count; the script asserts it.
The line count it prints is authoritative, so read it rather than guessing.

--retime-only recomputes the timing column from an EXISTING scene_breakdown.txt at a
measured rate, without re-chunking. Use it once a voiceover exists and its real rate
is known. Do NOT re-chunk at the new rate: the word band is derived from the rate, so
a different rate moves every boundary and invalidates every authored scene record.
"""
import argparse
import os
import re
import sys

# lane presets: words per minute, and the seconds band one generated clip covers
LANES = {
    "long": {"wpm": 145.9, "min_sec": 5.0, "max_sec": 8.0},
    "short": {"wpm": 174.0, "min_sec": 4.0, "max_sec": 6.0},
}

WORD = re.compile(r"[A-Za-z0-9'\u2019$-]+")
REBALANCE_PASSES = 30


def count(text):
    return len(WORD.findall(text))


def words(line):
    return [w for w in line.split(" ") if w]


def split_sentences(text):
    return [p.strip() for p in re.split(r"(?<=[.!?])\s+", text.strip()) if p.strip()]


def split_long(sentence, max_words):
    total = count(sentence)
    if total <= max_words:
        return [sentence]
    for sep in (r"(?<=,)\s+", r"(?<=;)\s+", r"(?<=:)\s+"):
        parts = [p.strip() for p in re.split(sep, sentence) if p.strip()]
        if len(parts) < 2:
            continue
        target = total / 2.0
        best, best_at, run = -1, 0, 0
        for i in range(len(parts) - 1):
            run += count(parts[i])
            if best < 0 or abs(run - target) < abs(best - target):
                best, best_at = run, i
        left = " ".join(parts[: best_at + 1])
        right = " ".join(parts[best_at + 1:])
        return split_long(left, max_words) + split_long(right, max_words)
    joins = [" and ", " but ", " because ", " to ", " of ", " in ", " with ", " that "]
    best_at, best_len = -1, float("inf")
    for join in joins:
        at = sentence.find(join)
        while at >= 0:
            pos = count(sentence[:at])
            if abs(pos - total / 2.0) < abs(best_len - total / 2.0):
                best_len, best_at = pos, at
            at = sentence.find(join, at + 1)
    if best_at > 0:
        left = sentence[:best_at].strip()
        right = sentence[best_at + 1:].strip()
        return split_long(left, max_words) + split_long(right, max_words)
    toks = sentence.split(" ")
    size = int(max_words)
    return [" ".join(toks[i:i + size]).strip() for i in range(0, len(toks), size)]


def chunk(script, minimum, maximum):
    units = []
    for s in split_sentences(script):
        units.extend(split_long(s, maximum))

    lines, current, cur_words = [], [], 0
    for unit in units:
        uw = count(unit)
        if cur_words == 0:
            current, cur_words = [unit], uw
            continue
        if cur_words + uw <= maximum:
            current.append(unit)
            cur_words += uw
            continue
        if cur_words >= minimum:
            lines.append(" ".join(current))
            current, cur_words = [unit], uw
            continue
        pieces = split_long(unit, maximum - cur_words)
        head = pieces[0]
        current.append(head)
        cur_words += count(head)
        lines.append(" ".join(current))
        rest = " ".join(pieces[1:]).strip()
        current, cur_words = ([rest], count(rest)) if rest else ([], 0)
    if current:
        lines.append(" ".join(current))

    # Capped rebalance. Uncapped, this oscillates on some scripts and hangs.
    for _ in range(REBALANCE_PASSES):
        moved = False
        i = 0
        while i < len(lines):
            here = count(lines[i])
            if here > maximum + 0.5:
                over = int(here - (maximum - 1))
                take = min(over, here - 8)
                if i > 0 and count(lines[i - 1]) + take <= maximum + 0.5:
                    w = words(lines[i])
                    lines[i - 1] = lines[i - 1] + " " + " ".join(w[:take])
                    lines[i] = " ".join(w[take:])
                    moved = True
                    i += 1
                    continue
                if i + 1 < len(lines) and count(lines[i + 1]) + take <= maximum + 0.5:
                    w = words(lines[i])
                    lines[i] = " ".join(w[: len(w) - take])
                    lines[i + 1] = " ".join(w[len(w) - take:]) + " " + lines[i + 1]
                    moved = True
                    i += 1
                    continue
            if here < minimum - 1.5:
                need = min(int(minimum - here) + 1, 9999)
                if i > 0:
                    prev = words(lines[i - 1])
                    take = min(need, len(prev) - 8)
                    if take > 0:
                        lines[i - 1] = " ".join(prev[: len(prev) - take])
                        lines[i] = " ".join(prev[len(prev) - take:]) + " " + lines[i]
                        moved = True
                        i += 1
                        continue
                if i + 1 < len(lines):
                    nxt = words(lines[i + 1])
                    take = min(need, len(nxt) - 8)
                    if take > 0:
                        lines[i] = lines[i] + " " + " ".join(nxt[:take])
                        lines[i + 1] = " ".join(nxt[take:])
                        moved = True
                        i += 1
                        continue
            i += 1
        if not moved:
            break
    return lines


def retime(bd_path, out_dir, wpm):
    """Recompute scene_timings.txt from an existing breakdown, at a measured rate."""
    lines = []
    with open(bd_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            m = re.match(r"^(\d+)\.\s*(.*)$", line)
            if not m:
                raise SystemExit(f"{bd_path}: line is not numbered: {line[:60]!r}")
            lines.append(m.group(2))
    out = os.path.join(out_dir, "scene_timings.txt")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(f"{i + 1}. {count(l) / wpm * 60:.2f}s"
                          for i, l in enumerate(lines)) + "\n")
    secs = [count(l) / wpm * 60 for l in lines]
    print(f"retimed {len(lines)} lines at {wpm:.1f} wpm | "
          f"total {sum(secs):.1f}s | avg {sum(secs) / len(secs):.2f}s")
    print(f"wrote {out} (scene_breakdown.txt was NOT touched)")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("script", help="script.txt, or the episode dir with --retime-only")
    ap.add_argument("out_dir", nargs="?")
    ap.add_argument("--lane", choices=sorted(LANES), default="long")
    ap.add_argument("--wpm", type=float, default=None)
    ap.add_argument("--min-sec", type=float, default=None, dest="min_sec")
    ap.add_argument("--max-sec", type=float, default=None, dest="max_sec")
    ap.add_argument("--retime-only", action="store_true", dest="retime_only")
    ap.add_argument("--duration", type=float, default=None,
                    help="measured voiceover duration in seconds. retime-only derives the "
                         "exact rate from it, which a rounded --wpm cannot reproduce")
    args = ap.parse_args()

    preset = LANES[args.lane]
    wpm = args.wpm if args.wpm is not None else preset["wpm"]
    min_sec = args.min_sec if args.min_sec is not None else preset["min_sec"]
    max_sec = args.max_sec if args.max_sec is not None else preset["max_sec"]
    minimum = wpm * min_sec / 60.0
    maximum = wpm * max_sec / 60.0

    if args.retime_only:
        episode = args.script
        bd_path = os.path.join(episode, "scene_breakdown.txt")
        if args.duration:
            # Rate to full precision, from the audio. A rounded wpm loses a centisecond
            # on every line whose exact value lands on a rounding boundary.
            if not os.path.exists(bd_path):
                raise SystemExit(f"missing {bd_path}")
            words = sum(count(re.sub(r"^\d+\.\s*", "", l.strip()))
                        for l in open(bd_path, encoding="utf-8") if l.strip())
            wpm = words / (args.duration / 60.0)
            print(f"derived rate {wpm:.4f} wpm from {words} words over {args.duration:.2f}s")
        return retime(bd_path, args.out_dir or episode, wpm)

    if not args.out_dir:
        raise SystemExit("out_dir is required unless --retime-only is used")

    script = open(args.script, encoding="utf-8").read()

    lines = chunk(script, minimum, maximum)

    total = sum(count(l) for l in lines)
    spoken = count(script)
    assert total == spoken, f"breakdown {total} words vs script {spoken}"

    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "scene_breakdown.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(f"{i + 1}. {l}" for i, l in enumerate(lines)) + "\n")
    with open(os.path.join(args.out_dir, "scene_timings.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(f"{i + 1}. {count(l) / wpm * 60:.2f}s" for i, l in enumerate(lines)) + "\n")

    secs = [count(l) / wpm * 60 for l in lines]
    print(f"lines {len(lines)} | words {total} == script {spoken} | "
          f"band {minimum:.1f}-{maximum:.1f} words at {wpm:.1f} wpm ({min_sec:.0f}-{max_sec:.0f}s)")
    print(f"avg {sum(secs) / len(secs):.2f}s  min {min(secs):.2f}s  max {max(secs):.2f}s  "
          f"total {sum(secs):.1f}s")
    print(f"wrote {args.out_dir}/scene_breakdown.txt and {args.out_dir}/scene_timings.txt")
    print("READ THE LINE COUNT ABOVE. That is how many scene records you author next.")


if __name__ == "__main__":
    sys.exit(main())
