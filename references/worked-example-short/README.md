# Worked example, SHORT (sixty seconds, stylised animation)

A real episode, finished and published, copied here unchanged. Nothing in it was
authored for this guide.

**What it is.** A sixty second animated history short about a homing pigeon that
carried a message out of a pocket of surrounded soldiers, lost an eye and a leg doing
it, and saved about two hundred men.

**The numbers.** 7 shot lines. 169 narration words. 5 declared identities, four
people and one animal. 58.3 seconds of narration at 174 words per minute.

## What is in here

| File | Note |
|---|---|
| `script.txt` | The narration. Note the hook: a number, first word |
| `script-tagged.txt` | One sentence per line, `[pause]` and `[emphasis]` only |
| `characters.txt` | Five identities, including the animal, in the animal shape |
| `character_prompts.txt` | One reference plate prompt per identity, plain white backdrop |
| `scene_breakdown.txt` | The script sliced into 7 shot lines |
| `scene_timings.txt` | The timing column |
| `movie_scene_prompts.txt` | 7 image prompts, `[NAME]` anchors, anchor footer |
| `animation_scene_prompts.txt` | 7 video prompts, `@NAME` anchors, same footer |
| `post.txt` | Caption plus hashtags |

There is no `scenes.txt` here. This lane hand-authored its prompt blocks directly
rather than generating them from records, which is why the gate reports its absence as
an advisory note rather than a failure. Both routes produce the same two files, and
the record route is the one this guide recommends, because it makes the 1 to 1
between breakdown lines and prompts true by construction.

`voice.mp3` is not here.

## Verify it

    python3 scripts/verify_documentary.py references/worked-example-short

It must print OK, with three advisory notes. All three are real and all three are
described below.

## What it predates, and the three things not to copy

This episode was made before the current house rules were tightened. Its format is
correct and its craft is good, and three specific numbers in it are out of date. The
authoring rules in this guide are the current ones, not this example's.

### 1. It has seven shots, not eleven to fourteen

Its lines run from 1.72 seconds to 12.41 seconds, mean 8.33 seconds. The current rule
is one 4 to 6 second clip per shot, because generated clips come back at 4 to 6
seconds and an 8 second line cannot be covered by a single clip.

Re-chunking the same script at the SHORT preset fixes it exactly:

    mkdir -p /tmp/short
    python3 scripts/chunk_scenes.py references/worked-example-short/script.txt \
        /tmp/short --lane short

That prints 12 lines, the band 11.6 to 17.4 words, an average of 4.86 seconds and a
total of 58.3 seconds, and 169 words, untouched: re-chunking moves boundaries and never
alters the words. Twelve shots carrying exactly the same narration that this example
carries in seven.

### 2. Its narration prints digits: `1918` and `194`

The current rule is years and figures as words. In narration that becomes `nineteen
eighteen` and `a hundred and ninety four`. Digits are allowed only in list metadata.
This is why the gate counts digit tokens.

### 3. Its `[pause]` tag is a line PREFIX, not a suffix

Line two opens with `[pause] That's roughly how many...`, where this guide's tagger
appends `[pause]` after the sentence. Both are silent to the TTS backend and both
satisfy the tags-parity check, so the gate accepts either. The suffix form is the one
this guide teaches because it is the one the long-form lane's proven episodes carry.

## What to copy from it

- **The hook.** First word is a number, second word is a unit: `Two hundred men.` No
  wind up, no statement of fact, no question.
- **The turn.** The myth set up and then broken in one line: `We love to say war is a
  human thing. But a bird with a hole through its chest flew forty kilometers because
  a note was taped to her.`
- **The ending.** A feeling, then a provocation, in five words: `She just knew it
  mattered.`
- **The animal entry in `characters.txt`.** It keeps the same shape as a person and
  swaps the clothing block for `Wearing a simple restraint: ..., no other clothing`.
- **The anchors doing the plural work.** `many @AMERICAN SOLDIER huddle` and `other
  @AMERICAN SOLDIER watch` rather than a pluralised anchor name, which is the rule.
- **The animation register's backdrop.** Pure white and warm studio lighting, against
  the documentary register's mid grey and overcast.

## Where it came from

One episode of a sixty second animated history shorts lane, sharing the production
engine with the long-form documentary lanes. Same file conventions, animation
register, plain white character plates.
