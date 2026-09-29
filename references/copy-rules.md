# Copy rules

Every rule below applies to EVERY file, including the script. They are not style
preferences and they are all checkable.

## The table

| Rule | Why |
|---|---|
| ZERO em dashes, ZERO en dashes | Read as machine punctuation in narration, and they break the metadata |
| ZERO double and ZERO curly quotes | No dialogue exists in this pipeline, so a quote character is a defect |
| ZERO question marks, in any file | A rhetorical question makes the sentence depend on the one after it |
| ZERO markdown bold, and no headings in `script.txt` | The only bold allowed is the identity heading in `character_prompts.txt` |
| NO second person: never `you`, `your`, `yours` | The voice is `we`, `they`, `he`, `she` |
| Years and figures as WORDS | Digits read inconsistently in TTS and force the caption pass to guess |

Digits are permitted in exactly two places: the list numbers in `characters.txt`, and
the `SC` numbers in `scenes.txt`. Everywhere else they are a defect.

## The dash rule in full

No em dash, no en dash, no hyphen used as a dash. Commas, semicolons, colons and
periods instead.

A hyphen inside a compound word is fine (`two decked`, `nineteen twenties` style
compounds are usually written open anyway). What is banned is the dash used as
punctuation.

## Why the question mark rule is absolute

The breakdown reproduces the script word for word, so a question in the script is a
question in a metadata file. Metadata files carry zero question marks by contract.

On the history and documentary lane the proven episode carries zero question marks in
ANY file, script included, because that lane's breakdown is a strict reproduction. So
a rhetorical question surviving into an approved script gets edited out, two
characters changed and the rhythm kept intact, and the edit is flagged with the
reversal offered rather than defended as a script voice exception.

Grep the proven episode in `worked-example-long/` for `?` before deciding a script
may use question hooks. It has none.

## Years and figures

Write `nineteen eighteen`, not `1918`. Write `forty kilometres`, not `40 km`. Write
`sixty four guns`, `twelve percent`, `a thousand three hundred metres`.

This reaches further than the script on a documentary lane: it also reaches the
headings in `character_prompts.txt`. `**Prompt 1, Vessel, 1975, ...**` is authored as
`nineteen seventy five`, and `1930s` as `nineteen thirties`. The digits that
legitimately remain are `Prompt 1` in the headings, the `1. NAME` list numbers, and
the `SC` numbers. Report both classes rather than leaving them unremarked.

## The one command

Run this on an episode folder and report the output verbatim. Every file must print
`CLEAN`, except that `character_prompts.txt` is expected to report `bold`, exactly
two per identity, because the bold heading is required there.

```python
import re, glob, os
files = ["script.txt", "characters.txt", "character_prompts.txt", "scenes.txt",
         "post.txt", "scene_breakdown.txt", "movie_scene_prompts.txt",
         "animation_scene_prompts.txt"]
for f in files:
    p = os.path.join("<episode_dir>", f)
    if not os.path.exists(p):
        print(f, "MISSING")
        continue
    t = open(p, encoding="utf-8").read()
    bad = {"dash": len(re.findall(r"[\u2014\u2013]", t)),
           "quote": len(re.findall(r'["\u201c\u201d\u2018\u2019]', t)),
           "qmark": t.count("?"),
           "2nd": len(re.findall(r"\b(you|your|yours)\b", t, re.I)),
           "bold": t.count("**")}
    print(f, {k: v for k, v in bad.items() if v} or "CLEAN")
```

`scripts/verify_documentary.py` runs this and everything else, and it knows that
`scenes.txt` legitimately carries the hyphen inside identity names, so point it at
the folder rather than hand-rolling the check.

## Metadata copy is not script copy

The metadata files (`characters`, prompts, post) additionally carry:

- Zero rhetorical questions. When a script line is a question, render the metadata
  beat as a statement.
- No hype vocabulary. No "incredible", no "shocking", no "mind blowing", no "you
  won't believe".
- No call to action and no subscription ask, anywhere.

Do not let short-form script voice guidance leak into metadata files, and do not let
metadata strictness flatten a script that is allowed to breathe.

## What is deliberately allowed

- **First person plural.** `we`, `our`, `much to our surprise`. House voice, and
  encouraged.
- **Impersonal construction.** The most common house voice on the documentary lane.
- **Commas inside a scene record field.** The comma is the refs separator, so a comma
  elsewhere in a field is fine.
- **Hyphens inside identity names.** `JEAN-BAPTISTE DENYS` is a legal name. The name
  regex includes the hyphen precisely so hyphenated names are not truncated.
- **Bold in `character_prompts.txt` headings only.**
