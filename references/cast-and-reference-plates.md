# The cast and the reference plates

Stage 5. Two files, and they are a pair: `characters.txt` is the identity, and
`character_prompts.txt` is the sheet the model actually sees.

## What a reference plate is for

One image per identity, generated ONCE, then passed as a reference on every scene
call that features that identity. That is what stops a face, a hull or an animal
drifting across a hundred shots. Without the plate the model re-invents the subject
every generation and the film reads as a slideshow of similar strangers.

So the plate has to pin the discriminators, in words, hard.

## Hard rules

- **Six identities maximum.** A production constraint, not a preference.
- **Every declared identity must appear in at least one shot.** One that never
  appears cost a wasted plate and draws an empty box in the cast strip. Do not
  declare something you only mention in prose.
- **Names must match `^[A-Z][A-Z0-9 \-]+$`.** Capitals, digits, spaces, hyphens. No
  apostrophes, periods, colons or plurals. An identity named `KING'S COMMISSIONER` is
  invisible to every parser here and every shot referencing it fails as undeclared.
  `CROWN COMMISSIONER` works.
- **Cast order is fixed in `characters.txt`** and is preserved downstream: the order
  of the blocks in `character_prompts.txt` and the order of the lines in the anchor
  footer.
- **The two files must declare the same cast in the same order.** The footer is built
  from one and the plates come from the other, so a name in one and not the other
  produces a footer entry with no sheet behind it.

## `characters.txt`

One numbered block per identity. An identity sheet, not a prompt and not an acting
direction. Stable traits only.

- No action verbs. No transient poses. No scene context. No bold.
- Answer "who is this", never "what are they doing".

```
1. NAME
Identity paragraph: era, age or period, build, materials and markings, what
makes the silhouette unmistakable, and what the reference sheet has to pin so the
model cannot hand back a variant.
```

**A person entry** describes age, gender, build, skin, hair, features, head to foot
clothing of the period, permanent props, default expression.

**A vessel or object entry** describes hull form, deck layout, funnel or turret count
and placement, superstructure, colour and weathering, and ends with an explicit
statement of what must NOT be shown: no legible lettering, no name, no pennant
number, no ensign, no crest.

**An animal entry** keeps the same shape, but the clothing block becomes "Wearing a
simple restraint: [collar, rope or harness details], no other clothing", and the
physical description carries feathers, fur, snout, hooves, ears and tail.

Real entry, vessel:

```
4. VASA
Royal warship, the Swedish hull of sixteen twenty eight. Two complete gun decks
with the lower ports cut close to the waterline, sixty four guns, a high full stern
with three tiers of carved and painted figures, an open beakhead forward, three
masts with a square rig. Planking pale tarred oak, the hull sides streaked with tar
and paint, the deck clutter of gun tackle and coiled rope, no legible lettering
anywhere. Rides tender, low in the water, the lower ports barely clear of the
surface. Built at the Stockholm yard and armed on royal order.
```

## `character_prompts.txt`

ONE file for the whole cast, ONE prompt per identity, in cast order. Not one file per
character and not five prompts each. If variations are wanted, add Prompt 2 onward
inside that character's own block.

````
NAME
**<emoji> Prompt 1, <Person or Vessel or Animal>, <age or year>, <short label>**
✨ Look: <one clause catching the identity's role in the story>

```text
<one full paragraph, a single prompt>
```
````

Use a distinct emoji per block. The bold heading is required here and is the only
bold allowed anywhere in the file set.

### Person, documentary register

Starts: `A full-body photorealistic character turnaround reference, rendered as
man/woman, about N years old, with believable human proportions and natural skin
texture,` then the physical description, then `Wearing ...` with the period clothing
head to foot, then `The surface is real ... with no gloss and no digital sheen.`,
then `Pose: .... Expression: .... Front facing and slightly angled views. Isolated on
a plain mid grey backdrop, soft overcast light, soft contact shadow under the feet,
centred composition, historically accurate <period> materials, no environment, no
props, no text, no extra characters.`

Real example:

```text
A full-body photorealistic character turnaround reference, rendered as man, about sixty years old, with believable human proportions and natural skin texture, ruddy weathered skin, deep lines at the eyes and mouth, grey stubble, broad shouldered with heavy forearms and callused hands. Wearing a coarse dark wool doublet, a linen shirt with an open collar, dark breeches, wool stockings, scuffed leather shoes, and a leather apron with a folding rule and a set of brass dividers in the pocket. A marking cord is coiled over one shoulder. The surface is real weathered skin and worn cloth, with no gloss and no digital sheen. Pose: standing facing forward, dividers in the right hand. Expression: heavy patience. Front facing and slightly angled views. Isolated on a plain mid grey backdrop, soft overcast northern light, soft contact shadow under the feet, centred composition, historically accurate 1620s northern European materials, no environment, no props other than the cord and dividers, no text, no extra characters.
```

### Vessel or object, documentary register

Starts: `A four view ship reference plate of <type>, <year>, with believable hull
proportions and worn surfaces, built from ...` then hull form, armament and deck
layout, superstructure, paint scheme and weathering, then `The surface is real ...`,
then `Four views: bow three quarter, full side ..., stern three quarter ..., and a
detail of .... Isolated on a plain mid grey backdrop, soft overcast light, soft
contact shadow under the hull, centred composition, historically accurate <period>
materials, no environment, no props, no text, no extra characters.`

Real example, and note the two clauses doing the real work: the count of decks is
stated, and `no legible lettering or name on the hull anywhere` is stated.

```text
A four view ship reference plate of a Swedish royal warship, 1628, with believable hull proportions and worn surfaces, built from tarred oak planking on a carvel hull, two complete gun decks with the lower tier of square ports cut very close above the waterline and the upper tier well above, sixty four guns, a bluff bow with a short beakhead and no figurehead, a very high full stern with three stacked galleries of carved and painted figures in red gold and blue, an open quarterdeck and poop, three masts with a square rig on the fore and main and a lateen on the mizzen, a short bowsprit, no legible lettering or name on the hull anywhere. Tarred dark oak with paint worn and streaked on the upperworks, fresh gilding on the stern, ironwork rusted, deck clutter of gun tackle and coiled rope. The surface is real weathered timber and flaking paint, with no gloss and no digital sheen. Four views: bow three quarter, full side showing both gun decks and the low waterline, stern three quarter showing the galleries, and a detail of the lower gun ports at the waterline. Isolated on a plain mid grey backdrop, soft overcast light, soft contact shadow under the hull, centred composition, historically accurate 1620s northern European materials, no environment, no props, no text, no extra characters.
```

### Person, animation register

```text
A full-body soft cinematic Pixar animation style character, designed as a man, in his early twenties, with smooth rounded shapes and subtle human facial features, soft smooth skin shading, fair skin with dirt smudges, short brown hair, square jaw, stubble, lean wiry build, and a charming, feature animation personality. The character has a human body with proportions similar to a modern feature animation film aesthetic. Wearing World War I American Expeditionary Forces clothing: olive drab wool tunic with high collar, canvas breeches, puttees wrapped around calves, brown leather boots, a steel Brodie helmet, a web belt with ammunition pouches, a small canvas message pouch on the belt. The character has smooth surfaces with subtle imperfections, and a soft tactile finish. Pose: standing facing forward. Expression: grim determination, exhausted but alert. Front-facing or slightly angled character turnaround reference look. Isolated on a pure white background, warm studio lighting, soft shadow under feet, centered composition, highly detailed, polished feature animation character model, clean character design, no environment, no props, no text, no extra characters.
```

### Animal, animation register

```text
A full-body soft cinematic Pixar animation style pigeon, designed as an adult homing pigeon, with smooth rounded shapes, soft smooth fur shading, iridescent gray and blue feathers with a white patch on the breast, missing right eye, a healed scar across the breast, sleek streamlined head with a small cere, slender body, and a charming, feature animation personality. Wearing a simple restraint: a thin leather collar with a small brass tag, no other clothing. The character has smooth surfaces with subtle imperfections, and a soft tactile finish. Pose: standing facing forward. Expression: steady, unwavering. Front-facing or slightly angled character turnaround reference look. Isolated on a pure white background, warm studio lighting, soft shadow under feet, centered composition, highly detailed, polished feature animation character model, clean character design, no environment, no props, no text, no extra characters.
```

Note the backdrop difference between the registers: mid grey and overcast for
documentary, pure white and warm studio for animation. Do not mix them.

## Making the plate actually pin the subject

The plate exists to prevent drift, so write the discriminators explicitly.

- **State what the object does NOT have, not only what it does.** A welded hull came
  back riveted because nothing forbade rivets. Write `no rivets` for welded, `no weld
  seams` for cast.
- **State the contour hard.** A cast hull came back boxier and taller than the real
  thing until the shape was described in firm words.
- **Pin the count.** Whenever a comparison the audience will make carries more of an
  item than the subject does, count it: `one funnel casing only`, `two gun decks`,
  `three masts`.
- **Name the defect you are preventing.** `or merged into the accommodation` stops
  two structures fusing.
- **State the gap.** `a bay of boxes between it and the deckhouse` holds an interval
  that the model will otherwise close.
- **Never name the comparison class inside the plate.** Comparing a hull to a famous
  class brings that class's own livery and its twin funnels along with it.
- **No signature in frame.** For any subject that carries markings, end the plate
  entry with what must not be shown.

A plate that is wrong is worse than a plate that is vague, because you will generate
art from it and then defend it. If a factual claim about a real subject is in doubt,
prove it against photographic evidence before rewording, and then re-run the gate to
prove nothing else broke.
