# Script craft

Stage 6. Two lanes, two registers, one word band each that does not move.

## The bands

| | SHORT | LONG |
|---|---|---|
| Words | 150 to 200 | 1,450 to 1,560 |
| Runtime | 50 to 66 seconds | 10 to 11 minutes |
| Narration rate | 175 to 185 wpm | 145 to 150 wpm |
| Shots, at 4 to 6s or 5 to 8s | 11 to 14 | 95 to 105 |

Both bands are roughly five percent wide. That is not enough headroom to drift into.

## Measure while you draft, not after

This is the single most expensive lesson available here. Drafts that measured
afterwards opened at 2,192, 2,454, 3,224 and 3,228 words against a 1,480 to 1,560
band, and every one of them paid a full rewrite. Drafts that measured as they went
landed inside the band on the first pass.

Three mechanisms, in order of how well they work.

### 1. Hold the paragraphs in code and count them for real

The one that landed a draft first pass. Assemble the paragraphs as a list, print the
word count of each paragraph and of the joined total, trim against those real
numbers, and gate the write on the band in the same step, so a draft that is out of
band never reaches the disk.

This exists because hand estimates of paragraph length ran a consistent six percent
low across five consecutive drafts. Never trust a hand count.

### 2. Derive the budget from the cap, not from taste

Decide the paragraph count first, then divide. At a 1,520 word target and a 25 to 40
paragraph contract, `1520 / 38` is 40 words per paragraph. Write the very first
paragraph to 35 to 40 words and the band is satisfied by construction rather than
repaired afterwards.

A pre-write budget alone is not enough, and on a third measurement it failed
outright: a draft that planned its paragraphs and its budgets before writing still
opened at 3,228 words. Budgeted paragraphs materialise at roughly twice the budget,
because the plan is measuring a script that does not exist yet.

### 3. Paragraph count is a second invariant that a word count cannot see

Four of five drafts in one measured run sat at or near the word band while sitting at
43 to 48 paragraphs, which is already out of band. A draft over the paragraph cap
needs a MERGE pass (two paragraphs joined, removing no words) BEFORE a cut pass. They
are separate dials, and running only the cut dial can never fix the count.

## Length is not a lever you can pull on the narration rate

A rate outside the target band does not mean editing the script. Rate is `words /
duration`, and reading rate is a property of the voice and the model, not of script
length: adding or removing words changes the runtime, not the words per minute. The
same voice and model measured 145.9 wpm on one episode and 151.4 on the next.

The only levers are a re-render, the tag density, or accepting it. Report the measured
figure, the runtime against the target, and the lever. Never cut prose to chase a
rate.

## The documentary register

The standard is dry, precise, engineering first, unhurried, no adjectives doing work
that numbers could do, and never talking down.

- **Open on a moment, a mechanism or a hard number.** Not a question. A question
  opener is banned by the copy rules anyway.
- **Structure as an argument.** What everyone believes, what the record shows, and
  why the gap matters. The correction is the spine.
- **Mechanism is the drama.** The rudder, the shell weight, the watertight
  subdivision, the sea state, the depth of the ice, the chemistry of the seabed.
- **Where the record is contested, say so and give both sides.** Do not pick the more
  dramatic account.
- **Close on consequence and on a portable lesson.** No call to action, no
  subscription ask, no second person, no summary that repeats what the audience just
  watched.
- **Medium length sentences. Concrete nouns.** No hype vocabulary. No "incredible",
  no "shocking", no "mind blowing".
- **Numbers are words.** "Sixty four guns", "twelve percent", "a thousand three
  hundred metres". Digits are allowed only in list metadata, never in narration.
- **First person plural is house voice.** "We", "our", "much to our surprise". It is
  allowed and encouraged. Second person is not.

## The animation and short register

Warmth carries it, and the whole film hangs on one turn.

- **Hook with the number or the twist in the first two seconds.** Retention collapses
  there, so the hook is the retention strategy.
- **Counterintuitive turn.** Set up what the audience thinks, then subvert it.
- **Conversational and slightly irreverent.** Tell it like a story to a friend, not
  like a lecture.
- **Compressed.** 150 to 200 words. No wasted words. Every line drives to the reveal.
- **Humanise, then provoke.** Land on a poignant image, then close with a claim
  someone will want to argue with. A flat factual ending generates no comments.
- **Self contained sentences.** Every sentence explains itself, because each shot
  line is a standalone shot and a sentence that needs the next one creates a phase
  gap between the image and the voice.

## The honesty rules

- **Do not let a rhetorical question survive into an approved script.** The breakdown
  reproduces the script word for word, so a question in the script becomes a question
  in a metadata file, where questions are banned. Rewrite it as a statement rather
  than defending it as a script voice exception.
- **Do not lift sentences from an in copyright book into a commercial script.**
  Emulate register, quote nothing. Check the jurisdiction before treating any source
  text as quotable; public domain is jurisdiction specific.
- **A section named in the ask is one section.** If someone asks for a breakdown of
  part one of a multi part script, that is part one alone. Prove the unit before any
  paid step.
- **Report cuts you notice rather than restoring them.** If the user edits the script
  in place between turns, their version is the master. Re-read it immediately before
  deriving anything from it, and never regenerate it from your own earlier copy.
