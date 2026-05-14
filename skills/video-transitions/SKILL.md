---
name: video-transitions
description: Adds transitions between video clips using ffmpeg xfade filter. Supports fade, dissolve, wipe, slide, zoom, and more. Trigger with /video-transitions when the user wants to add transitions between clips or to a single video.
intent: Takes one or multiple video clips and joins them with smooth transitions (fade, dissolve, wipe, slide, zoom, blur, etc.) using ffmpeg's xfade filter. Asks for clips, transition type, duration, and output path before executing.
type: interactive
---

# Video Transitions Skill

## Purpose

Join video clips with smooth transitions using ffmpeg's `xfade` filter. Works with 2 or more clips.

## Prerequisites Check

```bash
which ffmpeg && ffmpeg -filters 2>/dev/null | grep xfade || echo "MISSING: ffmpeg with xfade support (brew install ffmpeg)"
```

## Interaction Flow

Ask **one question at a time**.

### Step 1 — Get the video clips

Ask:
> "¿Cuáles son los videos que quieres unir con transiciones? Pega las rutas separadas por coma (o una sola si quieres agregar intro/outro fade):"

Verify each file exists:
```bash
ls -lh "<clip1>" "<clip2>" ...
```

If only one clip is provided, offer:
- Fade in al inicio
- Fade out al final
- Ambos

### Step 2 — Transition type

Ask:
> "¿Qué tipo de transición quieres?
> 1. fade — fundido a negro (clásico)
> 2. dissolve — fundido cruzado entre clips
> 3. wipeleft / wiperight — barrido horizontal
> 4. wipeup / wipedown — barrido vertical
> 5. slideleft / slideright — deslizamiento
> 6. zoom — zoom hacia adentro
> 7. fadeblack — fundido a negro
> 8. fadewhite — fundido a blanco
> 9. pixelize — efecto píxelado
> 10. Ver todas las disponibles"

If option 10, run:
```bash
ffmpeg -filters 2>/dev/null | grep xfade
```

### Step 3 — Transition duration

Ask:
> "¿Cuánto debe durar cada transición?
> 1. 0.5 segundos (rápida)
> 2. 1 segundo (recomendado)
> 3. 1.5 segundos
> 4. 2 segundos (suave)
> 5. Personalizado"

### Step 4 — Output path

Ask:
> "¿Dónde guardar el video final?
> 1. Misma carpeta del primer clip (nombre: output_with_transitions.mp4)
> 2. Escritorio
> 3. Ruta personalizada"

---

## Execution Pipeline

### Step A — Get clip durations

For each clip, get its duration in seconds:
```bash
ffprobe -v quiet -show_entries format=duration -of csv=p=0 "<clip>"
```

Store as: `duration_1`, `duration_2`, etc.

### Step B — Normalize clips (same resolution/fps)

Check if clips have the same resolution and fps:
```bash
ffprobe -v quiet -select_streams v:0 -show_entries stream=width,height,r_frame_rate -of csv=p=0 "<clip>"
```

If different, normalize all to match the first clip:
```bash
ffmpeg -i "<clip>" -vf "scale=<W>:<H>,fps=<FPS>" -c:v libx264 -c:a aac /tmp/clip_<N>_norm.mp4 -y
```

### Step C — Build xfade filter chain

For 2 clips with 1 transition:
```
offset = duration_1 - transition_duration
```

```bash
ffmpeg \
  -i "<clip1>" -i "<clip2>" \
  -filter_complex "
    [0:v][1:v]xfade=transition=<type>:duration=<dur>:offset=<offset>[v];
    [0:a][1:a]acrossfade=d=<dur>[a]
  " \
  -map "[v]" -map "[a]" \
  -c:v libx264 -c:a aac \
  "<output>" -y
```

For 3 clips with 2 transitions:
```
offset1 = duration_1 - transition_duration
offset2 = duration_1 + duration_2 - (2 * transition_duration)
```

```bash
ffmpeg \
  -i "<clip1>" -i "<clip2>" -i "<clip3>" \
  -filter_complex "
    [0:v][1:v]xfade=transition=<type>:duration=<dur>:offset=<offset1>[v01];
    [v01][2:v]xfade=transition=<type>:duration=<dur>:offset=<offset2>[v];
    [0:a][1:a]acrossfade=d=<dur>[a01];
    [a01][2:a]acrossfade=d=<dur>[a]
  " \
  -map "[v]" -map "[a]" \
  -c:v libx264 -c:a aac \
  "<output>" -y
```

Scale this pattern for N clips.

### Fade in/out for single clip

**Fade in:**
```bash
ffmpeg -i "<clip>" \
  -vf "fade=t=in:st=0:d=<dur>" \
  -af "afade=t=in:st=0:d=<dur>" \
  -c:v libx264 -c:a aac "<output>" -y
```

**Fade out:**
```bash
# Get duration first
DUR=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "<clip>")
FADE_START=$(echo "$DUR - <fade_dur>" | bc)

ffmpeg -i "<clip>" \
  -vf "fade=t=out:st=${FADE_START}:d=<fade_dur>" \
  -af "afade=t=out:st=${FADE_START}:d=<fade_dur>" \
  -c:v libx264 -c:a aac "<output>" -y
```

**Both fade in and fade out:**
```bash
ffmpeg -i "<clip>" \
  -vf "fade=t=in:st=0:d=<dur>,fade=t=out:st=${FADE_START}:d=<dur>" \
  -af "afade=t=in:st=0:d=<dur>,afade=t=out:st=${FADE_START}:d=<dur>" \
  -c:v libx264 -c:a aac "<output>" -y
```

---

## Available xfade Transitions

| Name | Effect |
|---|---|
| `fade` | Simple fade |
| `dissolve` | Cross dissolve |
| `wipeleft` | Wipe from right to left |
| `wiperight` | Wipe from left to right |
| `wipeup` | Wipe from bottom to top |
| `wipedown` | Wipe from top to bottom |
| `slideleft` | Slide new clip from right |
| `slideright` | Slide new clip from left |
| `slideup` | Slide new clip from bottom |
| `slidedown` | Slide new clip from top |
| `circlecrop` | Circle crop reveal |
| `rectcrop` | Rectangle crop reveal |
| `distance` | Distance effect |
| `fadeblack` | Fade through black |
| `fadewhite` | Fade through white |
| `radial` | Radial wipe |
| `smoothleft` | Smooth slide left |
| `smoothright` | Smooth slide right |
| `zoom` | Zoom effect |
| `pixelize` | Pixelate transition |
| `diagtl` | Diagonal top-left |
| `diagtr` | Diagonal top-right |
| `diagbl` | Diagonal bottom-left |
| `diagbr` | Diagonal bottom-right |

---

## Error Handling

| Error | Solution |
|---|---|
| `Unknown transition` | Check spelling; run `ffmpeg -filters \| grep xfade` for valid names |
| Black frames at cut | Recalculate offset: `offset = duration - transition_dur` |
| Audio desync | Ensure all clips have same sample rate before merging |
| Different resolutions | Normalize clips first with scale filter |
| `acrossfade` error | Clip audio may be shorter than transition — reduce transition duration |

## Anti-Patterns

- Don't skip duration/fps normalization — mismatched clips cause glitches.
- Don't set transition duration longer than the shortest clip.
- Don't use `copy` codec with xfade — it requires re-encoding.
- Show the command to the user before running it.
