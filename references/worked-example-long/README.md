# Worked example, LONG (ten to eleven minutes, photorealistic documentary)

A real episode, finished and published, copied here unchanged. Nothing in it was
authored for this guide.

**What it is.** One episode of a long-form photorealistic historical documentary
channel, about the Swedish warship that sank in her own harbour on her maiden voyage
in 1628. This is the gold standard the pipeline was calibrated against.

**The numbers.** 101 scenes. 1,591 narration words. 34 percent flagged ANIMATE, 67
HOLD. Five declared identities, against a ceiling of six. 76,464 bytes of image
prompts and 50,255 bytes of video prompts, both generated from `scenes.txt`.

## What is in here

| File | Note |
|---|---|
| `script.txt` | The narration, paragraph form, the register to match |
| `script-tagged.txt` | One sentence per line, `[pause]` and `[emphasis]` only |
| `characters.txt` | Five identities: three people and two vessels |
| `character_prompts.txt` | One reference plate prompt per identity, in cast order |
| `scenes.txt` | The 101 authored records, eleven fields each. This is the Stage 8 format |
| `scene_breakdown.txt` | The script sliced into 101 shot lines |
| `scene_timings.txt` | The timing column, retimed at the measured rate |
| `movie_scene_prompts.txt` | 101 image prompts, `[NAME]` anchors, anchor footer |
| `animation_scene_prompts.txt` | 101 video prompts, `@NAME` anchors, same footer |
| `beats.txt` | `lo,hi,HEAD` art book section headings, an optional extra |
| `post.txt` | Caption plus five hashtags |

`voice.mp3` is not here. It is about 15 MB and it belongs to the episode folder, not
to a guide. The timing column is the artifact that depends on it, and it is here.

## Verify it, and use it to prove your own gate

    python3 scripts/verify_documentary.py references/worked-example-long --wpm 151.4

It must print OK. If it does not, the gate is wrong, not the episode.

Prove the gate can fail, in a scratch copy, before trusting any PASS:

    cp -r references/worked-example-long /tmp/probe
    head -60 /tmp/probe/movie_scene_prompts.txt > /tmp/t
    mv /tmp/t /tmp/probe/movie_scene_prompts.txt
    python3 scripts/verify_documentary.py /tmp/probe --wpm 151.4

That must print three failures and exit 1.

## Prove the builder against it, which is the strongest test in this guide

The two prompt files here were generated from `scenes.txt` by the pipeline that built
the episode. Running the bundled builder over this folder must reproduce both files
byte for byte:

    mkdir -p /tmp/rebuild
    python3 scripts/build_scene_prompts.py references/worked-example-long \
        --register documentary --out /tmp/rebuild
    cmp /tmp/rebuild/movie_scene_prompts.txt \
        references/worked-example-long/movie_scene_prompts.txt
    cmp /tmp/rebuild/animation_scene_prompts.txt \
        references/worked-example-long/animation_scene_prompts.txt

Both compare clean, at 76,464 and 50,255 bytes. Same for the breakdown:

    mkdir -p /tmp/rechunk
    python3 scripts/chunk_scenes.py references/worked-example-long/script.txt \
        /tmp/rechunk --lane long --wpm 145.9
    cmp /tmp/rechunk/scene_breakdown.txt \
        references/worked-example-long/scene_breakdown.txt

And the timing column reproduces only when the rate is passed at full precision,
which is why the retime mode takes a measured duration rather than a rounded rate:

    mkdir -p /tmp/retime
    python3 scripts/chunk_scenes.py references/worked-example-long \
        --retime-only --duration 630.58 /tmp/retime

At `--wpm 151.4` that reproduces 84 of 101 lines and misses the other 17 by one
centisecond. At the precise rate derived from the duration it reproduces 101 of 101.

## What to watch for

**The script is 1,591 words, above the 1,480 to 1,560 band this guide teaches.** The
band was tightened after this episode was made. The gate reports it as an advisory
note, not a failure, which is the correct behaviour: a real published episode is
evidence, and a checker that fails its own reference file is broken.

**The timing column was retimed at 151.4 wpm, not the 145.9 wpm the script was
chunked at.** This is the one behaviour in the pipeline that looks like an
inconsistency and is not. The breakdown and the shots are frozen at the calibration
rate the script was authored to. Once the voiceover existed and its real duration was
measured, only the timing column was re-derived. Re-chunking at the new rate instead
moves every boundary and invalidates all 101 authored records.

**`script-tagged.txt` here opens on `[emphasis]On`.** That lane's own tagger tags the
literal first word, while the documented rule is the first CONTENT word. The bundled
`tag_script.py` follows the documented rule and would open on `[emphasis]tenth`.
Either satisfies the tags-parity check, which is what the gate enforces. Known,
deliberate, and not worth editing a published artifact over.

**The cast is five, not six.** That is normal and correct. Three people and two
vessels, and every one of them appears in at least one shot.

## Where it came from

One episode of a long-form maritime documentary channel on a shared production engine,
authored against that lane's own authoring contract. The register is photorealistic
historical documentary, the anchors are `[NAME]` for images and `@NAME` for video, and
the style lines are the documentary pair in `references/style-lines.md`.
