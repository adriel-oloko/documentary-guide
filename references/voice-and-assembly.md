# The handoff: voice, plates, stills, clips, edit

Stage 12. This guide stops at the file set. Everything below is the last mile, and
none of it is written for you, for one reason: it all costs money per attempt, and a
voice, a plate or a clip you have not looked at is one you cannot approve.

What you have when you leave the guide: nine files, verified, and a shot list with every
prompt written.

## 1. The voiceover

Render `script-tagged.txt`. The script IS the transcript, so never transcribe the audio
to recover text, and never wrap the audio in a container to read it.

### Tag syntax

Two tags only, and the renderer must be proved to ignore them silently rather than
speak them:

- `[pause]` where the read needs air before the next beat.
- `[emphasis]` prefixed directly to the stressed word or phrase, no closing tag.

Consolidate consecutive targets into one tag. Never tag the word `one`, which is far
too common as a pronoun to be a reliable target.

Prove the backend once per model: send a tiny tagged clip, transcribe it back, and grep
the transcript for the word "pause" or "emphasis". Absent means the tags are silent and
safe to send raw. If they come back spoken, the render is unusable and no amount of
editing fixes it.

Flatten the tagged file to single spaces before sending. One sentence per line is a
file convention, not an API requirement.

### Voice settings that have worked

Render settings that read as a narrator rather than a read-through: stability around
0.5, similarity around 0.75, speed between 0.95 and 1.0. Below 0.9 drags, above 1.05
reads as somebody reading a page.

Pick the voice by ear, not by name. Render the hook line in two or three candidates and
choose. Warm mid-range is the usual answer for documentary; the animation lane wants
more energy.

A cloned voice inherits the register of the clip it was cloned from, and a speed
parameter is often ignored by the model outright. If two clones come back too fast, do
not clone a third reference: move to a model that takes performance direction instead.

### Measure the rate, and do not chase it

Rate is `clean script word count / (duration in seconds / 60)`. Always the clean script,
never the tagged file, because tag tokens inflate the count.

Then write the measured rate back into `scene_timings.txt` by re-deriving the column
only:

    python3 scripts/chunk_scenes.py <episode_dir> --retime-only --duration 630.58

Do NOT re-run the chunker at the new rate: the chunker's word band is derived from the
rate, so a different rate re-chunks the script, moves the boundaries and invalidates
every authored scene record. Pass the measured duration rather than a rounded rate,
because a rounded rate loses a hundredth of a second on every line whose exact value
lands on a rounding boundary. On the worked long example, the duration reproduces the
real column 101 lines out of 101 and a rounded rate reproduces 84.

A rate outside the target band does not mean editing the script. Adding or removing
words changes the runtime, not the words per minute. The only levers are a re-render,
the tag density, or accepting it. Report the measured figure and the runtime against
target, and pick a lever.

### Two failure modes to expect

**An output file opened before the request returns leaves a zero byte file that the
next run reads as success.** An aborted or quota-rejected call leaves the mp3 at zero
bytes, and the re-run's "already exists" check then skips it. Delete an empty output
before retrying, and treat a 0.0 second duration as a failure rather than an existing
render.

**A full long-form render outruns a short command timeout.** Run it in the background
and poll, or the kill lands mid-request and produces the zero byte file above.

On a hosted API an HTTP payment error can mean either a billing state or a bad key, and
the two look identical. Separate them with a read-only balance call before diagnosing,
and never report a key problem you have not measured.

## 2. The reference plates

Generate one image per identity from `character_prompts.txt`, in the register's
backdrop, and keep them.

Do this before any scene still. They are passed as references on every scene call, and
every scene generated before them is a scene you will pay for twice.

## 3. The stills

One image per shot. Image prompt N against the refs in record N. The prompt file
already carries the anchors and the style line.

If a still comes back wrong, rewrite its prompt to describe what you actually got
before you regenerate, or the next attempt is the same mistake. The prompt file should
describe the image in hand, not the image you asked for.

Where a scene carries anchors and the result still drifts, the reference plate is the
thing to fix, not the scene prompt.

## 4. The clips

Generate ONLY the ANIMATE records. Give every HOLD record a slow 3 to 5 percent push in
instead. At documentary pacing a push in is visually indistinguishable from a generated
clip, and it is free, which is why the ANIMATE ratio is a cost decision made at Stage 8.

Before rendering anything, lock the stills. Every re-cut scene is paid for twice. Never
fire a video generation without an explicit order to spend.

Expected durations come from the generator, and they are not the same across models.
Match the shot length to what the model actually returns rather than to the shot list,
which is why the band matters more than an exact number.

Mute or bury the generator's own audio track, and steer it away from inventing one:
`No dialogue, no music, no subtitles, no new objects` is already the last line of every
video prompt.

## 5. Captions

Burn captions locally. Platform auto captions are not a substitute.

- **Text comes from `script.txt`.** Never from an ASR engine. The script is
  authoritative and a transcript only introduces drift.
- **Timing comes from the audio.** Map the script onto the audio with a sequence matcher
  over word level timestamps, and cache the result so re-runs are instant.
- **Cap each cue at 7 words and verify it programmatically.** Manual counting fails. A
  longer cue splits in two; a cue of two words or fewer merges into its neighbour unless
  it is a deliberate dramatic beat.
- White text that flips to a highlight colour on the currently spoken word, which is
  the karaoke treatment that reads best on a phone.
- **If the finished video exists but the source folder does not, you cannot caption it.**
  The script cannot be reliably re-derived from the audio, and transcribing it is
  forbidden. Keep the script and the voiceover folder with the render.

## 6. The edit

- **Lay the voiceover on the timeline first**, mark the shot boundaries against the
  waveform, then cut picture to those marks. Picture-first produces dead air.
- **Cut against the waveform, not the shot list.** Shot boundaries and caption cues are
  independent, and both follow the audio.
- **Export portrait 9:16** for social, or 16:9 for a documentary channel. Decide at
  Stage 3 and stay with it, because the safe areas differ.
- Re-check the length after assembly. Assembly reveals drift that the numbers did not.

## 7. Publish settings that the render depends on

- **Category: Education.** Not People and Blogs.
- **AI disclosure tick on every upload.** Mandatory, and it is not the thing that gets a
  channel penalised.
- **Not made for kids.**
- **Captions uploaded, not left to the platform.**
- **If the target market is in another timezone, schedule rather than post live.** For an
  operator in one timezone publishing to an audience in another, a fixed scheduled slot
  is the difference between an evening upload and a 4am one.
