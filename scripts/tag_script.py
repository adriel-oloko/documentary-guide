#!/usr/bin/env python3
"""Build the tagged TTS source from a clean script.

One sentence per line. Two tags only: [pause] after a sentence, and [emphasis]
prefixed to a target word. Consecutive target words take ONE tag. The words are never
altered, so stripping the tags reproduces the script exactly, and this script asserts
that before exiting.

Usage:
    python3 tag_script.py <script.txt> <out_tagged.txt> [--lane long|short]

Targets:
    leading numbers (digit or spelled)
    negations        no not never nothing nobody none isn't wasn't didn't can't don't
    contrast words   instead actually only secretly already yet barely impossible
    the first CONTENT word of sentence one, skipping articles and prepositions
The word "one" is never a target; it is far too common as a pronoun.
"""
import argparse
import re
import sys

NUMBER_WORDS = {
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
    "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
    "seventeen", "eighteen", "nineteen", "twenty", "thirty", "forty", "fifty",
    "sixty", "seventy", "eighty", "ninety", "hundred", "thousand", "million",
    "billion", "half", "quarter", "percent",
}
NEGATIONS = {
    "no", "not", "never", "nothing", "nobody", "none", "nowhere", "neither", "nor",
    "isn't", "wasn't", "didn't", "can't", "don't", "won't", "couldn't", "wouldn't",
    "shouldn't", "doesn't", "hasn't", "hadn't", "aren't", "weren't",
}
CONTRAST = {
    "instead", "actually", "only", "secretly", "already", "yet", "barely",
    "impossible", "almost", "still", "even", "exactly", "nearly", "just",
}
STOPWORDS = {
    "a", "an", "the", "in", "on", "at", "of", "for", "to", "from", "by", "with",
    "and", "but", "or", "so", "then", "now", "as", "it", "that", "this", "there",
}
TWIST_OPENERS = {
    "but", "so", "instead", "except", "yet", "however", "meanwhile", "then", "and",
    "for", "after", "in", "it", "that", "this", "there", "now",
}


def strip_punct(word):
    return re.sub(r"^[^A-Za-z0-9']+|[^A-Za-z0-9']+$", "", word).lower()


def split_sentences(text):
    return [p.strip() for p in re.split(r"(?<=[.!?])\s+", text.strip()) if p.strip()]


def targets_for(sentence):
    marks = []
    for p in sentence.split(" "):
        core = strip_punct(p)
        if not core:
            marks.append(False)
            continue
        if core[0].isdigit():
            marks.append(True)
        elif core in NEGATIONS or core in CONTRAST:
            marks.append(True)
        elif core in NUMBER_WORDS and core != "one":
            marks.append(True)
        else:
            marks.append(False)
    return marks


def hook_target(sentence):
    """Index of the first content word, skipping articles and prepositions."""
    for i, p in enumerate(sentence.split(" ")):
        core = strip_punct(p)
        if core and core not in STOPWORDS:
            return i
    return None


def tag_sentence(sentence, hook=False):
    parts = sentence.split(" ")
    marks = targets_for(sentence)
    if hook:
        i = hook_target(sentence)
        if i is not None:
            marks[i] = True
    if not any(marks):
        return sentence, 0
    # One emphasis run per line: keep the first run only, so the read stays house.
    runs, i = [], 0
    while i < len(marks):
        if marks[i]:
            j = i
            while j + 1 < len(marks) and marks[j + 1]:
                j += 1
            runs.append((i, j))
            i = j + 1
        else:
            i += 1
    if not runs:
        return sentence, 0
    start, end = runs[0]
    run = " ".join(parts[start:end + 1])
    prefix = "[emphasis]" if end == start else "[emphasis] "
    out = parts[:start] + [prefix + run] + parts[end + 1:]
    return " ".join(out), 1


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("script")
    ap.add_argument("out")
    args = ap.parse_args()

    script = open(args.script, encoding="utf-8").read()
    sentences = split_sentences(script)
    if not sentences:
        raise SystemExit("no sentences found in " + args.script)

    lines, emph = [], 0
    for n, s in enumerate(sentences):
        tagged, e = tag_sentence(s, hook=(n == 0))
        emph += e
        # House convention, taken from the proven episode: one sentence per line and
        # every sentence carries a trailing [pause]. The clean script is the source of
        # the words; the tag only says where the read may breathe.
        lines.append(tagged + " [pause]")

    tagged_text = "\n".join(lines) + "\n"

    def flatten_words(text):
        t = text.replace("[pause]", " ").replace("[emphasis]", " ")
        return t.split()

    if flatten_words(script) != flatten_words(tagged_text):
        raise SystemExit("FATAL: tagging changed the words. Refusing to write.")

    with open(args.out, "w", encoding="utf-8") as f:
        f.write(tagged_text)

    w = len(flatten_words(script))
    print(f"{args.out}: sentences {len(lines)} | [emphasis] {emph} | "
          f"[pause] {sum(1 for l in lines if l.endswith('[pause]'))} | words {w} identical to script")


if __name__ == "__main__":
    sys.exit(main())
