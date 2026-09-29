# Scene records

Stage 8. `scenes.txt`, one line per shot, eleven fields.

This file is the reason the counts match. One authored record per shot expands into
the image prompt, the video prompt and the art book entry, so the 1 to 1 between
breakdown lines and prompts is true by construction rather than by careful counting.
Nine episodes out of nine that were hand-written instead of generated drifted.

## The format

Fields separated by the three character sequence SPACE TILDE SPACE. The separator is
the tilde, so a tilde must never appear inside a field. Neither may a square bracket
or an at sign. A comma inside a field is fine and is the refs separator.

    n ~ label ~ flag ~ refs ~ place ~ use ~ emotion ~ action ~ movement ~ background ~ camera

| Field | What it is | Authored or derived |
|---|---|---|
| `n` | `SC1`, `SC2`, ... strictly sequential, no gaps | authored |
| `label` | Short clean editorial label, capitalised, 4 to 9 words | authored |
| `flag` | `ANIMATE` or `HOLD` | authored |
| `refs` | Comma separated declared identity names, or empty | authored |
| `place` | The setting clause, no `Place` prefix | authored |
| `use` | The lighting and camera treatment clause, no `Use` prefix | authored |
| `emotion` | The emotional register of the beat, a short noun phrase | authored |
| `action` | What physically happens in the frame | authored |
| `movement` | The motion clause: what moves, in what direction, how fast | authored |
| `background` | What sits behind the subject | authored |
| `camera` | The camera move | authored |

Real record:

```
SC1 ~ Royal warship at her moorings before the first voyage ~ HOLD ~ VASA ~ a tall two decked royal warship lying at her moorings in a crowded harbour at first light, gun ports open along both decks, rigging still and sails only beginning to draw, no legible lettering on the hull ~ low dawn light along the harbour water and a wide establishing shot from the quay ~ Quiet expectation on the morning of a disaster ~ The ship waits at her moorings ~ Harbour water moving slowly against the hull, pennants lifting in a light breeze ~ Wooden quays and sheds, moored small craft, the town rising behind ~ Wide from the quay, very slow push in
```

## The builder wraps your fields, so do not duplicate the wrapping

`build_scene_prompts.py` produces, per record:

**Image prompt**

```
SCENE N
Place <place>, using [NAME] from the uploaded references
Keep the exact design from the uploaded references.
Use <use>
<the style line for the register>
```

**Video prompt**

```
SCENE N
Scene: <label>, @NAME
Emotion: <emotion>
Action: <action>
Movement: <movement>
Background: <background>
Camera: <camera>
Style: <the style line for the register>
```

`No new objects` is appended automatically. Never write it yourself.

## The label

Authored, short and clean, 4 to 9 words. Never truncated automatically.

This matters more than it looks. An earlier version derived the label from the first
clause of the place field, truncating at fourteen words, and the place clauses run
long, so the derived labels produced broken phrases cut off mid preposition. Author
the label.

## ANIMATE versus HOLD: the shot economics

**ANIMATE** is one generated video clip. **HOLD** is a still with a slow 3 to 5
percent push in, which is free to move in the edit and visually indistinguishable at
documentary pacing.

| | LONG | SHORT |
|---|---|---|
| ANIMATE target | 30 to 50 percent | 60 to 80 percent |
| Clips | about 30 to 50 of 98 | 8 to 12 of 13 |

Assign ANIMATE to the hook, the beat transitions, the loss or discovery beats, and
anything where motion carries meaning. Assign HOLD to details, diagrams, charts,
portraits, textures and held landscapes.

A moving subject needs more ANIMATE than a static one. A vehicle or a battle episode
should budget 45 to 55 percent rather than reusing a ratio from a subject that mostly
stood still. Say which ratio you used and why, in the file, rather than leaving it to
be inferred.

## Empty refs

A record with nobody in frame still needs the field present, written as nothing
between two adjacent separators. Two spaces between the tildes:

```
SC4 ~ label ~ HOLD ~  ~ a dark dockyard store room with no water in frame ~ ...
```

A single tilde there makes ten fields, and ten fields is a hard failure downstream,
not a warning.

A scene with no cast in it is correct on the documentary lane and common on the
proven episodes. It is not a defect. Do not pepper a documentary reel with figures it
does not need. Pay for the empty scene with an explicit scale anchor and an explicit
behaviour clause, and write `no water in frame` on interiors so the requirement is
met visibly rather than silently skipped.

That is the direct opposite of the animation lane, where a scene with nobody in it
reads dead and drifts off the look. Give every animation scene at least one character
and one activity.

## Scale and behaviour, the two clauses that stop a plate looking fake

Open water renders as a flat plate or a repeating texture, horizons bend, and a hull
at an unknown distance reads as a model. The style line enforces neither. Both are
your job at write time.

- **Scale anchor, in `place`.** A human figure, a known hull length in words, a dock
  structure, a doorway, a sea state. Something whose size the audience already knows.
- **Behaviour clause, in `movement`.** How the water, smoke, fire or foliage actually
  moves, written out in full. `Harbour water moving slowly against the hull, pennants
  lifting in a light breeze`.

## Which refs go in which record

A record's refs should name the crew the place clause actually mentions, or the
reference sheet is paid for and used once. Nine bridge scenes that each described a
watch officer standing at the console, anchored on the interior sheet alone, left
that identity in a single record. Check the identity to scene counts before running
the builder, and remember that a single ANIMATE record in a group can be missed by a
find and replace keyed on one flag.

## Write it in one call

Write every record, start to finish, in one operation.

A half-written record is a hard stop: a line with ten fields instead of eleven makes
the builder assert and the whole episode stops there. And a file assembled by
appending is how a ninety six scene episode ends up with thirty eight records and a
truncated final line after the context or the budget runs out.

Author the records for a long episode in chunks of twelve to fourteen scenes into
separate files (`scenes-01.txt`, `scenes-02.txt`) if a single payload is too large to
write reliably. The builder reads them all in numeric order. What you must not do is
write one file partially.

## Number the labels first

The record count is the one invariant you cannot eyeball. Before authoring, write the
numbered label ledger and count it. A ninety seven scene episode was once authored as
eighty eight records because the beat plan in the author's head under-counted and
nothing in the writing flow noticed. It only surfaced when the builder asserted on
the beat count.

## Do not re-chunk after the fact

Once the records exist, the scene boundaries are frozen. Re-running the chunker at a
new rate moves the boundaries and invalidates every record. If a voiceover later
measures a different rate, re-derive `scene_timings.txt` only.
