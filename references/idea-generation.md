# Building and ranking an idea slate

Stage 2 of the pipeline. Ten ideas, ranked, then stop and let the user pick.

This step is skipped most often and it decides whether the film gets watched. A
correctly executed episode of a bad idea is a bad video.

## Why ten and not three

Three ideas is a shortlist and it forces a choice between whatever happened to come
to mind. Ten is a slate. At ten you start finding the ideas that only appear after
the obvious ones are written down, and the tenth is often better than the first.

Never present one idea. A single idea handed to a user is not a suggestion, it is a
decision made on their behalf.

## The five fields

No idea counts without all five. Write them out, do not summarise.

### 1. Slug

Lowercase, underscores. This becomes the folder name and the file name root.
`vasa_1628`, `boston_molasses_flood`, `wojtek_bear`. Not `The Vasa`, not `Vasa 1628`.

### 2. Subject

One line, plain, no spin. "The Vasa, the Swedish warship that sank in her own
harbour in 1628."

### 3. The angle

What happened, in the shape it will actually be told. If the angle is not a sentence
you could defend, the idea is not ready.

### 4. The hook line

The literal first sentence of the script. A number, a date or a moment. Write it out
in full, with the numbers spelled as words the way the copy rules require.

"On the tenth of August, in the year sixteen twenty eight, the largest warship
Sweden had ever built slipped her moorings in Stockholm harbour."

A hook you can only describe is not a hook, and a hook that opens with a statement
of fact rather than a number loses the first two seconds, where retention is
actually decided.

### 5. The correction

What the audience believes, and what the record shows. One line each.

If this field is empty, the idea is a listicle wearing a subject's clothes. Bin it
and write an eleventh.

## The ranking rules, and why they exist

These are measured, not taste. They came out of reading a channel's own retention
data across a published set.

### Paradox beats compliment

The winners were universally known subjects carrying a paradoxical or negative claim.
The flops were either niche subjects or complimentary claims.

So: a known ship plus "she sank in her own harbour on her maiden voyage" wins. The
same ship plus "the most powerful warship of her age" flops. The subject is what gets
the click. The claim is what keeps the watch.

This is the single most useful rule in the slate, and it is why field 5 is mandatory.

### Universal beats niche

A hull number is not an idea until the audience already cares about the hull. Order
the slate so the recognizable subjects come first and the deep cuts come later, once
there is an audience that will sit through a designation.

### Engineering forward stays ad safe

A mechanism story carries a catastrophe without a single body in frame. This matters
twice: it keeps the episode monetisable, and it makes the subject reachable at all.

### Familiarity is a ceiling, not a floor

The most famous subject in a family is often the worst opener, because you are
competing with a decade of established coverage on the same keyword. Save the obvious
one for later with a specific, non-generic angle. Never open with it.

### Leave two slots unassigned

Target a slate of about twelve and assign ten. By the time you have four or five
published episodes you will have real retention and click data, and the correct next
two subjects are whichever early episode overperformed, cloned.

Do not spend those slots on speculation now.

## Tiering

Once ranked, group into tiers and say what each tier is for:

- **Tier A, open with these.** Four to six entries. Universal, paradoxical, ad safe.
  These set the channel's identity.
- **Tier B, the body.** Recognizable, sound, slightly narrower. The workhorses.
- **Tier C, reserve.** The heaviest, strangest or most niche subjects. Held until
  there is authority to spend.

State the tier on every idea. A reviewer needs to know which ones are load bearing.

## Read the record before the tier, not after

Before an idea is promoted out of Tier C, check that its record exists. The subject
that sounds the most dramatic is frequently the one with a single thin source, and a
claim that traces to one popular retelling is not researchable.

Where the record is thin, say so. Where the record is contested, that is not a
dilution of the idea, it is the best possible episode: an argument the audience has
an opinion about.

## The do-not-do list

Applies to every family.

- **The most obvious subject as an opener.** Competing with a decade of established
  coverage.
- **Generic listicles.** "Ships through history", "foods that changed the world". No
  subject, no spine, no paradox.
- **Current conflicts.** A monetisation landmine and an accuracy minefield.
- **Pure glamour subjects.** Modern cruise launches, flagship launches with nothing
  wrong with them. No failure, no story.
- **Deep designations** until the audience will watch a designation.
- **Two ideas stacked into one episode.** The audience came for one thing.

## Output shape

Present the slate as a table plus a tier grouping:

| # | Slug | Subject | The angle | Tier | Risk |
|---|---|---|---|---|---|

Then, under it, the hook line and the correction for each of the Tier A entries
written out in full, because those are the ones the user will be deciding between.

Then one closing line: ask which one, and do not write a single file until the
answer comes back.

A full worked slate with the real reasoning is `idea-slate-example.md`.
