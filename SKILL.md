---
name: documentary-guide
description: Topic in, finished documentary file set out. Use when asked to make a documentary or history video on a topic, to suggest episode ideas, or to write the script, cast, scene breakdown and image and video prompt files. Covers ships, food, battles, animals, machines and disasters. Produces every text and prompt file the episode needs and never renders voice, images or video.
---

# The Documentary Guide

A topic goes in. A ranked slate of episode ideas comes out. You pick one, and this
guide writes every text and prompt file that episode needs.

It writes the thinking, the script, the cast, the shots and the prompts. It does
NOT write the voiceover, the images or the clips. Those are the last mile and they
are yours. Reasons in Stage 12, and it matters that you know it up front.

## The flow, at a glance

| Stage | What happens | Who decides |
|---|---|---|
| 1 | Topic, given or suggested | you |
| 2 | TEN ranked episode ideas | this guide, you pick |
| 3 | Shape and register locked | you |
| 4 | Research, myth against record | this guide |
| 5 | Cast | this guide |
| 6 | Script | this guide |
| 7 | Breakdown, timings, tagged script | scripts, derived |
| 8 | Scene records | this guide |
| 9 | Image and video prompt files | scripts, derived |
| 10 | Post caption | this guide |
| 11 | Verification | the gate |
| 12 | Voice, stills, clips, edit | you |

Stages 1 to 3 are conversation. Nothing is written to disk before you pick an idea.
Do not skip to Stage 6 because the subject sounds obvious.

## The file set this produces

Nine files, one folder named after the episode.

| # | File | What it is |
|---|---|---|
| 1 | `script.txt` | The narration, clean prose, paragraph form |
| 2 | `script-tagged.txt` | Same words, plus the two TTS tags |
| 3 | `characters.txt` | Cast identities, six maximum |
| 4 | `character_prompts.txt` | One reference-sheet prompt per identity |
| 5 | `scenes.txt` | One authored record per shot, eleven fields |
| 6 | `scene_breakdown.txt` | The script sliced into numbered shot lines |
| 7 | `scene_timings.txt` | Seconds of narration per shot line |
| 8 | `movie_scene_prompts.txt` | One image prompt per shot line |
| 9 | `animation_scene_prompts.txt` | One video prompt per shot line |
| 10 | `post.txt` | Caption plus hashtags |

Ten entries, and `voice.mp3` is deliberately not among them. A missing voiceover
makes the episode unrendered, not unfinished. Stage 12 says how to close it.

Files 6, 7, 9 and 10 are DERIVED. Never hand-write them. They come out of
`scripts/chunk_scenes.py` and `scripts/build_scene_prompts.py` so that the counts
match by construction rather than by careful counting.

## Stage 1: the topic

One topic per episode. Never stack two into one film.

Open by getting a topic. Three cases:

**The ask names a topic.** Take it. Say which family it lands in, and say whether the
family's failure mode is a risk for it.

**The ask is a family rather than a subject** ("ships", "food", "battles", "animals").
Go straight to Stage 2 and build the slate inside that family.

**The ask is open.** Offer these eight families, with the engine of each in one line,
then ask which one. Do not wait indefinitely and do not pick for them:

| Family | The engine of it | Where the record lives |
|---|---|---|
| Ships and shipwrecks | Naval architecture against the sea | Inquiry reports, wreck surveys, naval histories, museum records |
| Food | One ingredient or dish rewriting trade, empire or war | Trade archives, agricultural records, cookbooks, port ledgers |
| Battles | The plan, the ground, and the people inside it | Official histories, regimental diaries, after-action reports |
| Animals | A creature that did something history needed, or refused to | Newspaper archives, unit mascots, zoological records |
| Machines | One design that made everything before it obsolete | Patent offices, production tables, technical manuals |
| Disasters | A failure with a cause and a body count | Inquiry findings, engineering analyses, coroners reports |
| Medicine | The body, the trial, and the mistake | Journals, trial registries, hospital records |
| Money | A heist, a fraud, a crash, and who was holding the loss | Court filings, audit reports, period press |

Full detail per family, including real subjects and the failure mode each one carries,
is `references/topic-bank.md`. If the user wants to see the shape before committing to a
family, name two or three real subjects per family from that file rather than asking
them to choose blind.

A subject the user names that sits outside all eight families is still fine. Say which
family's engine you will tell it through, because the engine is what makes it an
episode.

## Stage 2: the idea slate

This is the step most people skip and it is the step that decides whether the film
gets watched. Produce TEN ideas. Never one. Then stop and let the user choose.

Five fields per idea, and no idea counts without all five:

1. **Slug.** Lowercase, underscores, the folder name. `vasa_1628`, not `The Vasa`.
2. **Subject.** One line, plain.
3. **The angle.** What happened, in the shape it will actually be told.
4. **The hook line.** The literal first sentence of the script: a number, a date or
   a moment. Write it out. A hook you can only describe is not a hook.
5. **The correction.** What the audience believes, and what the record shows. If you
   cannot fill this field, the idea is a listicle and it goes in the bin.

Then rank them and say why. The ranking rules are measured, not taste:

- **Paradox or negative claim beats a complimentary one.** Known subject plus a
  surprising or negative claim is what actually wins. Known subject plus praise is
  what flops.
- **Universal beats niche.** A hull number is not an idea until the audience already
  cares about the hull.
- **Engineering forward stays ad safe.** A mechanism story can carry a disaster
  without a single body in frame.
- **Leave two slots at the end unassigned.** By the time you have real retention
  numbers the right next subject is whichever early one overperformed, cloned.

Do not proceed on a single idea. Do not rank by which one you find most interesting.

A full worked slate, drawn from a real channel, is
`references/idea-slate-example.md`. The reasoning rules that produced it are in
`references/idea-generation.md`.

**Stop here.** Present the ten, ask which one, and wait. Everything below is
executed for one idea.

## Stage 3: shape and register

Two decisions, both locked before writing.

### Shape

| | SHORT | LONG |
|---|---|---|
| Runtime | 50 to 66 seconds | 10 to 11 minutes |
| Words | 150 to 200 | 1,450 to 1,560 |
| Shots | 11 to 14 | 95 to 105 |
| Seconds per shot | 4 to 6 | 5 to 8 |
| Words per shot | 12 to 19 | 12 to 20 |
| Narration rate | 175 to 185 wpm | 145 to 150 wpm |
| Cast ceiling | 6 | 6 |
| Animate ratio | 60 to 80 percent | 30 to 50 percent |

Choose SHORT for one strange fact with one turn in it. Choose LONG for a subject
with a mechanism, a sequence, and a consequence. If a SHORT idea needs four
corrections to explain itself, it is a LONG.

The word band is the one number that cannot drift. Both bands are about 5 percent
wide, so measure while drafting, not after. Drafts measured on the LONG lane opened
at 2,192, 2,454, 3,224 and 3,228 words against a 1,480 to 1,560 band, and each paid
a full rewrite. The drafts that measured as they went landed first pass.

### Register

Two registers exist. Pick one and never mix them, because the model will.

| | DOCUMENTARY | ANIMATION |
|---|---|---|
| Look | Photorealistic historical frame | Soft stylised feature animation |
| Use for | Ships, battles, disasters, machines | Animals, oddities, human-scale stories |
| Reference plate | Four view ship or object plate, or character turnaround | Character turnaround on plain white |

The style lines for each register are verbatim in `references/style-lines.md`. They
are the single most important strings in this whole pipeline. Copy them exactly. A
paraphrased style line is the most common quality failure there is, and a
generation that comes back looking realistic when it should look animated, or the
reverse, means the line was dropped or reworded.

## Stage 4: research, myth against record

Do this before writing the script, always. Prose written before the belief is
checked launders belief into fact, and the audience for this kind of film already
half knows the subject, so a laundered fact is the thing they will notice.

Write `00-research.md` first, with four sections:

    ## Myth against record
    | Belief | What the record shows | Source |
    (four rows minimum, a real source on every row)

    ## The spine
    (the mechanism the episode is actually about, one paragraph)

    ## Numbers worth saying out loud
    (each figure, and how you will write it in words)

    ## What is genuinely unresolved
    (the arguments with no agreed answer, so the script states both sides)

Three to five corrections is the normal yield, and the corrections are not a detour,
they are the payoff. The honest version is sharper than the myth. Rules and the
source hierarchy are `references/research-and-record.md`.

If you cannot source a number, do not use the number. Never invent a source, a
date, a dimension or a quote. Some subjects have no hero designer and no single
invention moment. Say so explicitly in the research file, or a later edit will
invent one to make the story land.

## Stage 5: cast

Six identities maximum, and this is a production constraint, not a preference.
Every declared identity must appear in at least one shot, or you have paid for a
reference sheet that is never used and drawn an empty box in the cast strip.

For the documentary register the convention is two or three people plus three or
four vessels or objects. A vehicle anchors as well as a face, and for a machine it
anchors BETTER, because the failure mode is variant drift (wrong funnel count,
wrong turret layout) rather than a slightly different face.

Names must match `^[A-Z][A-Z0-9 \-]+$`. Capitals, digits, spaces and hyphens only.
No apostrophes, no periods, no colons, no plurals. `KING'S COMMISSIONER` is
invisible to every parser in this pipeline; `CROWN COMMISSIONER` works.

`characters.txt` holds an identity paragraph per entry, stable traits only, no
action verbs and no scene context. `character_prompts.txt` holds one full
reference-sheet prompt per entry, in the same order.

Formats, both registers, plus the vessel and animal variants:
`references/cast-and-reference-plates.md`.

## Stage 6: the script

Write to the band in Stage 3. The copy rules in `references/copy-rules.md` apply to
the script too, and they are stricter than you expect: no dashes of any kind, no
quote characters, no question marks, no second person, and every year and figure
written as words.

Then measure. `wc -w script.txt` on the clean file, never on the tagged file,
because the tag tokens inflate the count. Fix the file until it is inside the band
and report the final number.

The register, for the documentary lane:

- Open on a moment, a mechanism or a hard number. Not a question.
- Structure the episode as an argument: what everyone believes, what the record
  shows, and why the gap matters.
- Mechanism is the drama. The rudder, the subdivision, the sea state, the depth of
  the ice, the chemistry of the seabed.
- Where the record is contested, say so and give both sides. Do not pick the more
  dramatic account.
- Close on consequence and a portable lesson. No call to action, no subscription
  ask, no second person.

Register detail for both lanes, and the paragraph maths that keeps a long draft
inside a 5 percent band, is `references/script-craft.md`.

## Stage 7: derive the breakdown, timings and tagged script

Run the chunker. It is authoritative for the scene count, so you do not guess it.

    python3 scripts/chunk_scenes.py <slug>/script.txt <slug> --wpm 145.9

It prints the line count and asserts that the words across the lines equal the
script word count. READ THE LINE COUNT IT PRINTS. That number is the number of
scene records you now have to author.

Then tag:

    python3 scripts/tag_script.py <slug>/script.txt <slug>/script-tagged.txt

Two tags only, `[pause]` and `[emphasis]`. The words themselves are never altered,
so stripping the tags reproduces the script exactly, and the tagger asserts it.

Do not re-run the chunker after a voiceover exists. Re-chunking at a new rate moves the
boundaries and invalidates every authored scene record. Re-derive the timing column
only, and pass it the MEASURED duration rather than a rounded rate, or every line whose
exact value lands on a rounding boundary loses a hundredth of a second:

    python3 scripts/chunk_scenes.py <slug> --retime-only --duration 630.58

It reads the existing `scene_breakdown.txt`, leaves it alone, and rewrites only
`scene_timings.txt`. On the worked long example that reproduces the real timing column
101 lines out of 101; at a rounded rate it reproduces 84.

## Stage 8: scene records

One line per shot in `scenes.txt`, eleven fields, separated by the three character
sequence SPACE TILDE SPACE.

    n ~ label ~ flag ~ refs ~ place ~ use ~ emotion ~ action ~ movement ~ background ~ camera

Write it in ONE call, every record, start to finish. A half-written record is a
hard stop downstream, and a file built by appending is how a 96 scene episode ends
up with 38 records and a truncated final line.

A record with nobody in frame still needs the empty field present, written as
nothing between two separators:

    SC4 ~ label ~ HOLD ~  ~ the place clause ~ ...

Field-by-field detail, the ANIMATE versus HOLD economics, and the scale and water
rules that stop a seascape rendering as a flat plate are `references/scene-records.md`.

## Stage 9: build both prompt files

    python3 scripts/build_scene_prompts.py <slug> --register documentary --wpm 145.9

It reads the records, reads the narration beat for line N out of
`scene_breakdown.txt`, and writes both prompt files with the anchor footer. The 1 to
1 between breakdown lines, image prompts and video prompts is then true by
construction and cannot drift, which is the whole reason the records exist instead
of hand-written prompt blocks.

Two anchor files exist because the two generators need different syntax: image
prompts reference `[NAME]`, video prompts reference `@NAME`. Both carry the same
footer, byte for byte.

Anchor rules, the ones that break renders:

- Block letter name only. Never an inline description, never a redesign.
- Every ref used in a body appears in the footer, and every footer name is declared
  in `characters.txt`.
- Never pluralise or possess an anchor. `[GERMAN SOLDIER] figures on the ridge`, not
  `[GERMAN SOLDIER]s`. `the halter of [INCITATUS]`, not `[INCITATUS]'s halter`.
- A shot with no cast in it is fine and common. The footer lists only the identities
  that appear somewhere in the file.
- No dialogue, no quote characters, no dashes.

## Stage 10: post

Four to six short paragraphs, then exactly five hashtags. The caption states the
hook, the correction and the consequence in plain language, first person plural or
impersonal, no question mark, no second person, no hype.

Format and the hashtag pool: `references/post-and-publishing.md`.

## Stage 11: verify

Do not hand this over unverified.

    python3 scripts/verify_documentary.py <folder>

Point it at an episode folder, or at a folder whose children are episode folders. It
infers the lane from the script length unless you tell it which one, so a folder
holding both a sixty second episode and a ten minute one verifies both correctly with
the right bands.

It checks file presence, the script word band, breakdown concatenation against
`script.txt`, tag parity, the 1 to 1 prompt count, anchor completeness, the byte
identical footers, the cast ceiling, every declared identity actually used, the exact
style line once per scene, and the copy rules on every file. Fix what it flags, then run
it again.

Run it once with the measured rate after a voiceover exists, or the timing column
reports a note against the wrong rate:
`--wpm 151.4`, not the 145.9 default.

A FAIL from a freshly written checker is a hypothesis, not a finding. If the checker
is new, prove it on the worked example in `references/worked-example-long/` first: a
checker that fails its own reference file is broken, not a discovery.

## Stage 12: handoff, and the four things this does not do

This guide stops at the file set. The remaining work is:

1. **The voiceover.** Render `script-tagged.txt` through a TTS model, save as
   `voice.mp3`, then read its duration and derive the narration rate as script words
   divided by minutes. Write that rate back into the timings file. This is left out
   on purpose: it costs money per attempt, it is the one step where the model choice
   is a feel decision rather than a spec decision, and a voice you have not heard is
   a voice you cannot approve. Settings and the tag syntax: `references/voice-and-assembly.md`.
2. **The reference plates.** One image per identity in `character_prompts.txt`, at
   the register's backdrop. Generate these first and keep them. They are passed as
   references on every later scene call, and they are what stops a face or a hull
   drifting.
3. **The stills.** One image per shot, image prompt N against the record's refs.
4. **The clips and the edit.** Generate only the ANIMATE shots. Give every HOLD shot
   a 3 to 5 percent push in instead; at documentary pacing it is indistinguishable
   and it is free. Then cut against the voiceover waveform, not against the shot
   list.

Never let an ASR engine supply caption text. `script.txt` is the transcript. If
`voice.mp3` is the only thing you have and the script is gone, the script is not
recoverable from the audio and you should re-author it, not transcribe it.

## Pitfalls

- Do not write files before the user picks an idea. Ten in, one out.
- Do not start a script before the myth against record table exists.
- Do not draft first and measure the word count afterwards. Measure as you go.
- Do not plan length in paragraphs. Paragraph density is not a constant; it has been
  measured from 41 to 76 words per paragraph on one lane.
- Do not hand-write the derived files. Regenerate them.
- Do not write a scene record with ten fields, or with a tilde, a square bracket or
  an at sign inside a field. A comma inside a field is fine.
- Do not pluralise or possess an anchored name.
- Do not put dialogue or quote characters into a prompt file.
- Do not drop or paraphrase a style line.
- Do not let one character in `characters.txt` go unused in the shots.
- Do not stub a file to make a folder look finished. Say which file is missing.
- Do not generate images, video or voice without an explicit order to spend.

## Reference files

| File | Contents |
|---|---|
| `references/topic-bank.md` | The eight topic families, their engines, their failure modes |
| `references/idea-generation.md` | How to build and rank a slate, and why the ranking rules are what they are |
| `references/idea-slate-example.md` | A real twelve subject slate with tiers, and the do-not-do list |
| `references/style-lines.md` | The verbatim style lines for both registers |
| `references/research-and-record.md` | Source hierarchy, the myth table, the honesty rules |
| `references/script-craft.md` | Register, structure and length control for both lanes |
| `references/cast-and-reference-plates.md` | `characters.txt` and `character_prompts.txt`, people, vessels, animals |
| `references/scene-records.md` | The eleven fields, ANIMATE versus HOLD, scale and water |
| `references/copy-rules.md` | Every hard copy rule, with the one command that checks them |
| `references/verification.md` | What the gate checks and how to read a FAIL |
| `references/voice-and-assembly.md` | The handoff: TTS, plates, stills, clips, captions, publish |
| `references/post-and-publishing.md` | Caption format, hashtags, posting slots |
| `references/worked-example-short/` | A real 60 second episode, all nine files |
| `references/worked-example-long/` | A real ten minute episode, all nine files |
