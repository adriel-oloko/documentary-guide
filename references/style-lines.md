# The style lines, verbatim

The single most important strings in this pipeline. Copy them exactly, character for
character. A paraphrased style line is the most common quality failure there is.

If a generation comes back looking realistic when it should look animated, or
animated when it should look realistic, or smooth and plastic when it should look
worn, the style line was dropped or reworded. Put it back exactly.

Two registers. Pick one per episode and never mix them.

---

## REGISTER ONE: DOCUMENTARY (photorealistic)

Use for ships, battles, disasters, machines, medicine, money. The register says:
real world, real camera, real light.

### The image line

Goes at the end of every image prompt, in full:

```
Rendered as an ultra photorealistic historical documentary frame, cinematic realism, practical lighting, authentic textures, muted earth-tone color palette, subtle Kodak Vision3 film look, soft natural contrast, fine organic film grain, high dynamic range without artificial HDR, historically accurate materials and costumes, shallow depth of field only where physically appropriate, 35mm cinematic lens, 16:9, no text, no logos, no captions.
```

### The video line

Label this one `Style:` and put it last in every video prompt:

```
Style: Photorealistic historical documentary style, practical available light, authentic weathered textures, muted earth tone palette, fine organic film grain, no gloss, no digital sheen.
```

### The reference line

Goes on any prompt that carries anchors:

```
Keep the exact design from the uploaded references.
```

Singular "design". Not "designs".

### The audio line

Goes at the end of every video prompt, because the generator will otherwise invent
music and dialogue:

```
No dialogue, no music, no subtitles, no new objects.
```

---

## REGISTER TWO: ANIMATION (stylised feature animation)

Use for animals, oddities, human scale stories where the warmth carries the film.
The register says: soft, rounded, charming, clearly animated. Not claymation, not
stop motion, not photoreal.

### The image line

Goes at the end of every image prompt, in full:

```
Rendered in clean cinematic stylized Pixar animation style, highly detailed.
```

### The video line

Label this one `Style:` and put it last in every video prompt:

```
Style: Soft pixar animation style, smooth surfaces, subtle imperfections, practical studio lighting, shallow depth of field, tactile animated film aesthetic.
```

### The reference line

Same as the documentary register, and it still says "design", singular:

```
Keep the exact design from the uploaded references.
```

### The audio line

Same as the documentary register:

```
No dialogue, no music, no subtitles, no new objects.
```

---

## Register, materials and the write time rule

The style line holds the overall look. It does not hold a specific material, and it
does not hold scale. Both of those are your job at write time, and both fail silently
if you skip them:

- **Materials.** State what the object does NOT have, not only what it does. A welded
  hull came back riveted because nothing forbade rivets. Write "no rivets" for welded
  and "no weld seams" for cast.
- **Scale.** Every place clause needs an explicit scale anchor: a human figure, a
  known length in words, a dock structure, a sea state, a doorway.
- **Behaviour.** Water, smoke, fire and foliage get an explicit behaviour clause
  written out in full. A solver that is not told how the water behaves returns a flat
  plate or a repeating texture.
- **Text.** No in-frame signage, placards, charts, stencilled unit numbers, lettering
  or legible writing, and where an object would naturally carry writing, say it is
  blank. The no-text clause in the suffix does not survive an object that implies
  writing.

Verbatim suffixes are also written into `scripts/build_scene_prompts.py`. The script
is the authority the generated files actually use; this file is the authority a human
copying blocks by hand uses. If you change one, change the other, and note that
`verify_documentary.py` checks that every prompt file ends on the exact expected line.
