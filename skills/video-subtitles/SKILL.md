---
name: video-subtitles
description: Transcribes a video with Whisper and generates subtitles in multiple languages using translation. Burns subtitles into the video or exports as SRT/VTT files. Trigger with /video-subtitles when the user wants to add subtitles or captions in any language.
intent: Full subtitle pipeline — transcribes audio with Whisper, translates to target languages using AI, generates SRT/VTT files, and burns subtitles into the video with ffmpeg. Supports style customization (font, size, color, position) and multi-language output in one run.
type: interactive
---

# Video Subtitles Skill

## Purpose

Transcribe any video, translate to multiple languages, and either burn subtitles into the video or export as SRT/VTT files.

## Prerequisites Check

```bash
which ffmpeg  || echo "MISSING: ffmpeg (brew install ffmpeg)"
which whisper || echo "MISSING: whisper (pip install openai-whisper)"
```

For translation, Claude is used directly — no extra tools needed.

## Interaction Flow

Ask **one question at a time**.

### Step 1 — Get the video

Ask:
> "¿Cuál es la ruta del video al que quieres agregar subtítulos?"

```bash
ls -lh "<video_path>"
```

### Step 2 — Source language

Ask:
> "¿En qué idioma está el video?
> 1. Español
> 2. Inglés
> 3. Portugués
> 4. Francés
> 5. Auto-detectar (Whisper lo detecta solo)"

### Step 3 — Target languages

Ask:
> "¿En qué idioma(s) quieres los subtítulos? (puedes elegir varios)
> 1. Español
> 2. Inglés
> 3. Portugués
> 4. Francés
> 5. Alemán
> 6. Italiano
> 7. Japonés
> 8. Chino (simplificado)
> 9. Árabe
> 10. El mismo idioma del video (sin traducción)"

Accept multiple selections, e.g. "1, 2, 3".

### Step 4 — Whisper model

Ask:
> "¿Qué modelo de Whisper para la transcripción?
> 1. tiny — muy rápido
> 2. base — rápido
> 3. small — balanceado (recomendado)
> 4. medium — preciso
> 5. large — máxima precisión"

### Step 5 — Output format

Ask:
> "¿Qué quieres como resultado?
> 1. Subtítulos quemados en el video (hardcoded)
> 2. Solo archivos SRT (para reproductores externos)
> 3. Solo archivos VTT (para web)
> 4. Todo — video con subtítulos + SRT + VTT"

### Step 6 — Style (only if burning into video)

Ask:
> "¿Cómo quieres que se vean los subtítulos?
> 1. Estilo YouTube (blanco, fondo negro semitransparente, abajo)
> 2. Estilo cine (blanco con sombra, centrado abajo)
> 3. Estilo TikTok (grande, amarillo, centrado)
> 4. Personalizado (especifica fuente, tamaño, color)"

---

## Execution Pipeline

### Step A — Extract audio

```bash
ffmpeg -i "<video>" -vn -acodec pcm_s16le -ar 16000 -ac 1 /tmp/audio_sub.wav -y
```

### Step B — Transcribe with Whisper

```bash
whisper /tmp/audio_sub.wav \
  --model <model> \
  --output_format srt \
  --output_dir /tmp/whisper_subs \
  --language <source_lang>
```

Output: `/tmp/whisper_subs/audio_sub.srt`

Show a preview of the first 5 lines of the SRT to the user.

### Step C — Translate SRT to target languages

For each target language, read the SRT file and translate only the text lines (not the timestamps or sequence numbers).

SRT format:
```
1
00:00:01,000 --> 00:00:04,500
This is the subtitle text

2
00:00:05,000 --> 00:00:08,200
Another subtitle line
```

Rules for translation:
- Keep sequence numbers unchanged
- Keep timestamps unchanged
- Translate ONLY the text lines
- Preserve line breaks within a subtitle block
- Keep natural, conversational tone

Save translated SRT as:
```
<video_dir>/subtitles/<video_name>.<lang_code>.srt
```

Example: `video_es.srt`, `video_en.srt`, `video_pt.srt`

### Step D — Convert SRT to VTT (if requested)

```bash
ffmpeg -i "<file>.srt" "<file>.vtt"
```

VTT format starts with `WEBVTT` header — ffmpeg handles this automatically.

### Step E — Burn subtitles into video

#### Style: YouTube
```bash
ffmpeg -i "<video>" \
  -vf "subtitles=<srt_file>:force_style='FontName=Arial,FontSize=18,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,BorderStyle=3,Outline=1,Shadow=0,Alignment=2'" \
  -c:v libx264 -c:a copy \
  "<output_dir>/<name>_<lang>_subtitled.mp4" -y
```

#### Style: Cinema
```bash
ffmpeg -i "<video>" \
  -vf "subtitles=<srt_file>:force_style='FontName=Arial,FontSize=20,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,BorderStyle=1,Outline=2,Shadow=1,Alignment=2'" \
  -c:v libx264 -c:a copy \
  "<output_dir>/<name>_<lang>_subtitled.mp4" -y
```

#### Style: TikTok
```bash
ffmpeg -i "<video>" \
  -vf "subtitles=<srt_file>:force_style='FontName=Arial,FontSize=28,PrimaryColour=&H00FFFF,OutlineColour=&H000000,BorderStyle=1,Outline=3,Bold=1,Alignment=10'" \
  -c:v libx264 -c:a copy \
  "<output_dir>/<name>_<lang>_subtitled.mp4" -y
```

### Step F — Multi-language output

If multiple languages requested, run Step E for each language with its corresponding SRT file. Name outputs clearly:
```
video_es_subtitled.mp4
video_en_subtitled.mp4
video_pt_subtitled.mp4
```

---

## SRT Color Reference (ASS/SSA format used by ffmpeg)

| Color | Code |
|---|---|
| Blanco | `&HFFFFFF` |
| Amarillo | `&H00FFFF` |
| Cian | `&HFFFF00` |
| Verde | `&H00FF00` |
| Rojo | `&H0000FF` |
| Negro | `&H000000` |

Note: ffmpeg uses BGR order (reversed from RGB).

## Language Codes for filenames

| Language | Code |
|---|---|
| Español | `es` |
| Inglés | `en` |
| Portugués | `pt` |
| Francés | `fr` |
| Alemán | `de` |
| Italiano | `it` |
| Japonés | `ja` |
| Chino | `zh` |
| Árabe | `ar` |

---

## Output Directory Convention

```
<video_dir>/subtitles/
  audio_sub.es.srt        # Spanish SRT
  audio_sub.en.srt        # English SRT
  audio_sub.es.vtt        # Spanish VTT
  audio_sub.en.vtt        # English VTT

<video_dir>/
  <name>_es_subtitled.mp4   # Video with Spanish burned-in subs
  <name>_en_subtitled.mp4   # Video with English burned-in subs
```

---

## Error Handling

| Error | Solution |
|---|---|
| `No such file or directory` (SRT) | Check `/tmp/whisper_subs/` — filename may differ |
| `Unable to open file` in subtitles filter | Use absolute path for SRT file |
| Characters not rendering (Japanese/Arabic) | Add `FontName=NotoSansCJK` or `FontName=Noto Sans Arabic` |
| Subtitles out of sync | Re-run Whisper with a larger model |
| `Subtitle codec not supported` | Convert SRT with `ffmpeg -i file.srt file.vtt` first |

## Anti-Patterns

- Don't translate timestamps — only translate text content in SRT files.
- Don't burn multiple languages into the same video — create separate files per language.
- Don't hardcode font paths — use font names that are system-available.
- Show SRT preview to user before burning into video — let them spot errors.
- Don't use `copy` for video codec when burning subtitles — requires re-encoding with `libx264`.
