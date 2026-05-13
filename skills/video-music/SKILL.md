---
name: video-music
description: Adds background music to a video using ffmpeg. Controls volume mixing, fade in/out, loop, trim, and replaces or blends with original audio. Trigger with /video-music when the user wants to add music or a soundtrack to a video.
intent: Takes a video and an audio/music file, mixes them with configurable volume levels for both tracks, applies fade in/out to the music, and outputs a new video. Also supports replacing original audio entirely or looping short music tracks to match video duration.
type: interactive
---

# Video Music Skill

## Purpose

Add background music or a full soundtrack to any video using ffmpeg. Mix, replace, fade, loop — full control over the audio blend.

## Prerequisites Check

```bash
which ffmpeg || echo "MISSING: ffmpeg (brew install ffmpeg)"
```

## Interaction Flow

Ask **one question at a time**.

### Step 1 — Get the video

Ask:
> "¿Cuál es la ruta del video al que quieres agregar música?"

```bash
ls -lh "<video_path>"
```

### Step 2 — Get the music file

Ask:
> "¿Cuál es la ruta del archivo de música? (MP3, WAV, M4A, AAC, FLAC)"

```bash
ls -lh "<music_path>"
```

If the user doesn't have a music file, suggest free sources:
- **Pixabay Music**: pixabay.com/music (free, no attribution)
- **YouTube Audio Library**: studio.youtube.com/channel/music
- **Free Music Archive**: freemusicarchive.org

### Step 3 — Audio mode

Ask:
> "¿Cómo quieres manejar el audio original del video?
> 1. Mezclar — mantener audio original + agregar música de fondo
> 2. Reemplazar — quitar audio original, solo música
> 3. Solo música en partes sin voz (avanzado)"

### Step 4 — Volume levels (only if mixing)

Ask:
> "¿Qué volumen quieres para cada pista? (escala 0.0 a 1.0)
> 1. Audio original: 1.0 / Música: 0.2 (música sutil de fondo)
> 2. Audio original: 0.8 / Música: 0.4 (equilibrado)
> 3. Audio original: 0.5 / Música: 0.5 (mitad y mitad)
> 4. Personalizado"

### Step 5 — Music fade

Ask:
> "¿Quieres que la música tenga fade in/out?
> 1. Sí — fade in al inicio (2s) + fade out al final (3s)
> 2. Solo fade out al final
> 3. Sin fade"

### Step 6 — Output path

Ask:
> "¿Dónde guardar el video final?
> 1. Misma carpeta del video (nombre: video_con_musica.mp4)
> 2. Escritorio
> 3. Ruta personalizada"

---

## Execution Pipeline

### Step A — Get durations

```bash
# Video duration
VIDEO_DUR=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "<video>")

# Music duration
MUSIC_DUR=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "<music>")

echo "Video: ${VIDEO_DUR}s | Music: ${MUSIC_DUR}s"
```

### Step B — Mix audio (keep original + add music)

Basic mix with volume control:
```bash
ffmpeg -i "<video>" -i "<music>" \
  -filter_complex "
    [0:a]volume=<vol_video>[a_orig];
    [1:a]volume=<vol_music>[a_music];
    [a_orig][a_music]amix=inputs=2:duration=first[a_out]
  " \
  -map 0:v -map "[a_out]" \
  -c:v copy -c:a aac \
  "<output>" -y
```

### Step C — Replace original audio

```bash
ffmpeg -i "<video>" -i "<music>" \
  -map 0:v -map 1:a \
  -c:v copy -c:a aac \
  -shortest \
  "<output>" -y
```

### Step D — Loop music if shorter than video

If `MUSIC_DUR < VIDEO_DUR`:
```bash
ffmpeg -i "<video>" -stream_loop -1 -i "<music>" \
  -filter_complex "
    [0:a]volume=<vol_video>[a_orig];
    [1:a]volume=<vol_music>,atrim=duration=<VIDEO_DUR>[a_music];
    [a_orig][a_music]amix=inputs=2:duration=first[a_out]
  " \
  -map 0:v -map "[a_out]" \
  -c:v copy -c:a aac \
  "<output>" -y
```

### Step E — Add fade in/out to music

```bash
FADE_OUT_START=$(echo "<VIDEO_DUR> - 3" | bc)

ffmpeg -i "<video>" -stream_loop -1 -i "<music>" \
  -filter_complex "
    [0:a]volume=<vol_video>[a_orig];
    [1:a]volume=<vol_music>,
         afade=t=in:st=0:d=2,
         afade=t=out:st=${FADE_OUT_START}:d=3,
         atrim=duration=<VIDEO_DUR>[a_music];
    [a_orig][a_music]amix=inputs=2:duration=first[a_out]
  " \
  -map 0:v -map "[a_out]" \
  -c:v copy -c:a aac \
  "<output>" -y
```

### Step F — Trim music to start at a specific point

If the user wants to start the music at a specific timestamp (e.g., skip intro):
```bash
-itsoffset <skip_seconds> -i "<music>"
# or
-ss <skip_seconds> -i "<music>"
```

---

## Volume Reference

| Value | Effect |
|---|---|
| `0.0` | Silencio |
| `0.1` | Casi inaudible |
| `0.2` | Fondo suave |
| `0.4` | Fondo notable |
| `0.5` | Igual que original |
| `0.8` | Prominente |
| `1.0` | Volumen original |
| `1.5` | +50% amplificado |
| `2.0` | Doble de volumen |

---

## Common Recipes

### Música de fondo sutil (recomendado para tutoriales)
```bash
ffmpeg -i video.mp4 -stream_loop -1 -i music.mp3 \
  -filter_complex "[0:a]volume=1.0[v];[1:a]volume=0.15,afade=t=in:st=0:d=2,afade=t=out:st=<END-3>:d=3,atrim=duration=<DUR>[m];[v][m]amix=inputs=2:duration=first[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac output.mp4 -y
```

### Solo música, sin audio original
```bash
ffmpeg -i video.mp4 -stream_loop -1 -i music.mp3 \
  -map 0:v -map 1:a -c:v copy -c:a aac -shortest output.mp4 -y
```

### Música que termina con el video (fade out automático)
```bash
ffmpeg -i video.mp4 -stream_loop -1 -i music.mp3 \
  -filter_complex "[1:a]atrim=duration=<DUR>,afade=t=out:st=<END-3>:d=3[m];[0:a][m]amix=inputs=2:duration=first[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac output.mp4 -y
```

---

## Error Handling

| Error | Solution |
|---|---|
| `Audio shorter than video` | Add `-stream_loop -1` before `-i <music>` to loop |
| `No audio stream` | Video has no audio — use replace mode instead of mix |
| Out of sync | Use `-c:v copy` to avoid re-encoding video |
| Clipping/distortion | Reduce both volumes (e.g. 0.7 + 0.2) |
| `amix` outputs silence | Check filter_complex syntax — missing semicolons are common |

## Anti-Patterns

- Don't set `vol_music > 0.5` for background music — it will overpower speech.
- Don't re-encode video unnecessarily — use `-c:v copy` when possible.
- Don't forget `-stream_loop -1` when music is shorter than video.
- Show the final command to the user before running it.
- Always calculate `FADE_OUT_START` dynamically from video duration, never hardcode it.
