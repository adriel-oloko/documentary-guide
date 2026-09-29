# documentary-guide

A topic goes in. A ranked slate of episode ideas comes out. You pick one, and the
guide writes every text and prompt file that episode needs.

It does not write the voiceover, the images or the clips. Those are the last mile
and they stay yours.

## How to use it

**Pasting into a chat (Claude, ChatGPT, DeepSeek, anything).** Paste `SKILL.md`
first. That is the whole pipeline. Then give it a topic, or ask it for one, and
work through the stages in conversation.

Open a file from `references/` only when the stage you are on points at it. You do
not need to paste the whole folder.

**Handing it to a coding agent (Claude Code, Codex, Hermes, anything with a
terminal).** Point it at this folder and say which stage you are on. The scripts in
`scripts/` are what make the counts match by construction instead of by careful
counting, and the agent should be running them rather than rewriting their logic.

## Layout

    SKILL.md                    the pipeline. Read this first.
    README.md                   this file
    references/
      topic-bank.md             the eight topic families
      idea-generation.md        how to build and rank an idea slate
      idea-slate-example.md     a real twelve subject slate, with tiers
      style-lines.md            the verbatim style lines, both registers
      research-and-record.md    myth against record, and the source hierarchy
      script-craft.md           register, structure, length control
      cast-and-reference-plates.md   characters.txt and character_prompts.txt
      scene-records.md          the eleven field scene record
      copy-rules.md             every hard copy rule
      verification.md           what the gate checks
      voice-and-assembly.md     the handoff steps that are not this guide
      post-and-publishing.md     caption, hashtags, slots
      worked-example-short/     a real 60 second episode, all nine files
      worked-example-long/      a real ten minute episode, all nine files
    scripts/
      chunk_scenes.py           script -> scene_breakdown.txt + scene_timings.txt
      tag_script.py             script.txt -> script-tagged.txt
      build_scene_prompts.py    scenes.txt -> both prompt files
      verify_documentary.py     the gate. run this last, and again after any edit

## The scripts

All four take plain paths. Relative or absolute, no configuration, no house
folders, standard library only.

    python3 scripts/chunk_scenes.py  <script.txt> <out_dir> --lane long --wpm 145.9
    python3 scripts/chunk_scenes.py  <episode_dir> --retime-only --duration 630.58
    python3 scripts/tag_script.py    <script.txt> <out_tagged.txt>
    python3 scripts/build_scene_prompts.py <episode_dir> --register documentary --wpm 145.9
    python3 scripts/verify_documentary.py  <episode_dir>

`chunk_scenes.py --retime-only` recomputes the timing column from an existing
breakdown at a measured voiceover duration, without re-chunking. It reproduces the real
column in `references/worked-example-long/` 101 lines out of 101; a rounded `--wpm`
reproduces 84, which is why the duration is the parameter to pass.

`build_scene_prompts.py` takes `--register documentary` or `--register animation`, and
`--refs tail|inline` to choose between appending the anchors to the place clause and
expecting them inline. Both are shown in the worked examples.

`verify_documentary.py` works on an episode folder, or on a folder of episode folders,
and infers each episode's lane from its script length unless you pass `--lane`.

## The worked examples are real

Both are finished, rendered, published episodes, copied unchanged. Nothing in them
was authored for this guide. Read them when a format question comes up and you want
the real shape rather than a description of it.

Each carries a `README.md` naming where it came from and what it predates, so a
fault in the example is never copied as a rule.

## The one rule worth memorising

Never put a dash of any kind into any file, including the script. No em dash, no en
dash. Commas, semicolons, colons and periods instead.
