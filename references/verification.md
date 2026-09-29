# Verification

Stage 11. Run the gate, fix what it flags, run it again. Do not hand the episode over
unverified.

    python3 scripts/verify_documentary.py <episode_dir>

Point it at a single episode folder, or at a folder of episode folders the way
`references/worked-example-long/` is laid out, and it walks the children.

## What the gate checks

| Check | What it catches |
|---|---|
| File presence | Ten files expected, one named if missing |
| Script word band | `wc -w` of `script.txt` against 1,450 to 1,560, or 150 to 200 for SHORT |
| Breakdown concatenation | The numbered breakdown lines, prefixes stripped, must equal `script.txt` word for word |
| Scene line count | Breakdown non blank lines, and the count reported |
| Timing sum | The `N. X.XXs` column must sum against words divided by the rate |
| Tag parity | Stripping the two tags from `script-tagged.txt` reproduces `script.txt` exactly |
| Tag inventory | No tag other than `[pause]` and `[emphasis]` anywhere |
| Prompt count | `SCENE N` labels in each prompt file against breakdown lines, plus counted b-scenes |
| Prompt order | Labels sort into SCENE 1, 2, 3, 3b, 4 |
| Anchor completeness | Every ref in a body appears in that file's footer |
| Anchor declaration | Every ref appears in `characters.txt` |
| Footer identity | The two footers are byte identical |
| Cast ceiling | Six identities maximum |
| Cast used | Every declared identity appears in at least one record |
| Cast order | `characters.txt` and `character_prompts.txt` declare the same names in the same order |
| Empty refs field | Every record has eleven fields, empty refs included |
| Style lines | Every prompt file ends each block on the exact expected style line for its register |
| Copy rules | Dashes, quote characters, question marks, second person, bold |

Two checks need saying out loud.

**The style line check is the one that catches the most common failure.** A dropped or
paraphrased style line makes a whole episode render in the wrong register, and nothing
else notices, because the episode is otherwise perfect.

**The footer identity check is byte level.** Both prompt files must carry the same
`---` plus `ANCHOR TAGS` plus `[NAME] = @` block. A single differing line means one of
them was hand-edited.

## Two flags for the two real cases

`--bscenes <n>` tells the gate that n extra shots were inserted after their parent
blocks, so the label count is legitimately breakdown lines plus n. Labels must be
LOWERCASE: `SCENE 3b` is valid, `SCENE 3B` is a FAIL.

`--wpm <rate>` sets the rate used for the timing sum. Use the MEASURED rate from the
rendered voiceover, not the default. At the default rate the timing column reports a
false FAIL as soon as a voiceover exists at a different pace.

## A FAIL from a new checker is a hypothesis, not a finding

This is the pitfall that wastes the most time.

If the gate is freshly written, or you have just edited it, prove it on a known good
input first. Point it at `references/worked-example-long/` and `worked-example-short/`,
both of which are real and both of which must come back PASS. A checker that fails its
own reference file is broken, and reporting its output as a discovery sends you off to
fix a file that was never wrong.

Two real examples of a checker crying wolf, both from the same session: a parser that
required a blank line before every name line skipped block one, because the file starts
on line one by contract. And a second parser that sliced each block body to end of
file counted every later block's code fence, reporting ten of eleven blocks as failed
with bogus stray fence errors. The file was correct both times.

## The trap where the gate reports OK having checked nothing

Two ways this happens, and both look like success:

**A folder with no `scene_breakdown.txt` is skipped as a non-project folder.** So a
folder carrying the script, the cast and both prompt files but no breakdown reports OK
while proving nothing. A missing breakdown must always be a FAIL, never a skip.

**Pointing the walker at a project folder instead of its parent.** Given a project
folder it walks that folder's children, finds no episode subdirectory, prints nothing
and still exits zero. Pass the episode folder to `verify_documentary.py`, or the parent
to the multi episode mode, and read the line count it processed.

## The negative control

Prove the gate is live before trusting a PASS. In a scratch copy of a good episode,
truncate `movie_scene_prompts.txt` to half its blocks and confirm the gate prints FAIL.
A gate that has never been seen to fail has not been tested.

## What the gate cannot see

Three things, all of which need a human or a second check.

**The prose in `character_prompts.txt`.** No gate reads it. A wrong factual claim about
a real subject therefore ships green. Prove a contested claim about a real subject
against photographic or documentary evidence before rewording, then run the gate to
prove nothing else broke.

**A record whose refs the builder used, but whose place clause mentions a crew member
who is not anchored.** The gate checks that every ref is declared. It cannot check that
you anchored the right people. Count identity appearances per record before building.

**A prompt file that lost its refs tail.** A hand-authored movie block with a `Place`
line but no `, using [REFS] from the uploaded references` tail is not caught by ref
completeness, because that check runs the other way. If you hand-edit a block, check
that the bracket refs in the movie block equal the refs in its video block, and that
any block with refs carries the tail.

## The gate that lies about the timings once a voiceover exists

The timing column is derived from words divided by a rate. Before a voiceover exists,
the default rate is the best estimate. After it exists, the rate is measurable and the
default becomes a false FAIL. Re-derive the timings from the measured duration, and
pass `--wpm` the measured figure.

The gate reports a missing `voice.mp3` as a FAIL. That is correct behaviour and not a
bug: an episode with no voiceover is an unrendered episode, not a finished one. The
report should say so in one line, plus the command that closes it.
