---
name: video-highlights
description: Takes a video file, defines an editorial objective, transcribes it with Whisper, uses AI to identify the best segments aligned to the goal, and extracts them with ffmpeg. Trigger with /video-highlights when the user wants to find highlights or best moments from a video.
intent: Objective-first highlight extraction pipeline: define goal → audio extraction → Whisper transcription → AI analysis aligned to objective → ffmpeg segment extraction → optional highlight reel. Every editorial decision (which moments, how long, what tone) is driven by the stated objective.
type: interactive
---

# Video Highlights Skill

## Purpose

Take any video, define a clear editorial objective, transcribe it, and extract the segments that best serve that goal — not just the "best" moments in the abstract.

## Prerequisites Check

```bash
which ffmpeg   || echo "MISSING: ffmpeg (brew install ffmpeg)"
which whisper  || echo "MISSING: whisper (pip install openai-whisper)"
```

## Interaction Flow

Ask **one question at a time**.

### Step 0 — Define the editorial objective (ALWAYS FIRST)

**Default: el usuario crea YouTube Shorts / Reels.** Si no especifica otro destino, asumir YouTube Shorts automáticamente y confirmar brevemente:

> "Voy a editar esto como YouTube Short (máx 60s, vertical 9:16, gancho en los primeros 3s). ¿Correcto, o quieres otro formato?"

Si el usuario quiere cambiar, ofrecer:
> 1. **YouTube Short / Reel** ← default (máx 60s, 9:16, gancho en 3s)
> 2. YouTube video largo (resumen: intro + puntos clave + cierre)
> 3. LinkedIn (tono profesional, insight destacado, 1–3 min)
> 4. Trailer o teaser
> 5. Presentación o demo
> 6. Educativo (el "aha moment", paso a paso)
> 7. Objetivo personalizado

**Specs que se aplican automáticamente para YouTube Shorts:**
- Duración objetivo: **30–60 segundos**
- Resolución de salida: **1080x1920** (recortar vertical con `crop=1080:1920` si el source es horizontal)
- Gancho obligatorio: el **primer segmento** debe funcionar sin contexto previo
- Tono: dinámico, directo, sin introducciones largas
- El clip más valioso va **primero**, no al final

Store the objective. **Every subsequent decision is guided by this objective:**
- Which moments to select
- How long each clip should be
- What tone to prioritize
- Target duration of the final output
- Whether to crop to vertical (9:16)

### Step 1 — Get the video file

Ask:
> "¿Cuál es la ruta del video que quieres analizar?"

Accept absolute or relative paths. Verify the file exists:
```bash
ls -lh "<video_path>"
```

### Step 2 — Transcription model

Ask:
> "¿Qué modelo de Whisper quieres usar?
> 1. tiny — muy rápido, menos preciso (recomendado para pruebas)
> 2. base — rápido, buena precisión
> 3. small — balanceado (recomendado)
> 4. medium — más preciso, más lento
> 5. large — máxima precisión, lento"

### Step 3 — Selection criteria

Ask:
> "¿Qué tipo de momentos quieres extraer?
> 1. Los más interesantes / engaging
> 2. Los más informativos (datos, insights, enseñanzas)
> 3. Los más divertidos / entretenidos
> 4. Los más emotivos
> 5. Resumen general (mejores partes del inicio, medio y final)
> 6. Personalizado — describe tú mismo qué buscar"

### Step 4 — Duration target

Ask:
> "¿Cuánto debe durar el highlight reel aproximadamente?
> 1. 30 segundos
> 2. 1 minuto
> 3. 3 minutos
> 4. 5 minutos
> 5. Sin límite — extrae todo lo relevante"

### Step 5 — Output

Ask:
> "¿Qué quieres como resultado?
> 1. Clips individuales por segmento
> 2. Un solo video con todos los highlights unidos
> 3. Ambos"

---

## Execution Pipeline

### Step A — Extract audio

```bash
ffmpeg -i "<video_path>" -vn -acodec pcm_s16le -ar 16000 -ac 1 /tmp/audio_extract.wav -y
```

### Step B — Transcribe with Whisper

```bash
whisper /tmp/audio_extract.wav \
  --model <model> \
  --output_format json \
  --output_dir /tmp/whisper_out \
  --language Spanish
```

If language is unknown, omit `--language` and let Whisper auto-detect.

Output file will be at `/tmp/whisper_out/audio_extract.json`.

### Step C — Parse transcription

Read the JSON output. Each segment has:
```json
{
  "id": 0,
  "start": 12.5,
  "end": 18.2,
  "text": "...transcribed text..."
}
```

Build a readable transcript with timestamps and present it to the user:
```
[00:12] Texto del segmento...
[00:18] Siguiente segmento...
```

### Step D — AI analysis (objective-driven)

Analyze the full transcript with the **stated objective** as the primary filter. Do not just pick "interesting" moments — pick moments that serve the goal.

For each selected segment evaluate:

- **start**: timestamp inicio (seconds)
- **end**: timestamp fin (seconds)
- **reason**: por qué sirve al objetivo específico
- **score**: relevancia al objetivo 1-10
- **hook_potential**: ¿funciona como gancho de apertura? (sí/no)

**Objective-specific selection rules:**

| Objetivo | Priorizar | Evitar |
|---|---|---|
| Instagram/TikTok | Frases impactantes, reacciones, puntos de acción | Contexto largo, silencios |
| YouTube resumen | Intro, 3 puntos clave, llamada a acción | Digresiones, repeticiones |
| LinkedIn | Insight único, dato concreto, aprendizaje | Humor informal, lenguaje coloquial |
| Trailer/Teaser | Momentos de tensión o sorpresa, el clímax | Resoluciones, spoilers |
| Presentación/Demo | Demostración del producto, resultado final | Setup técnico, errores |
| Educativo | Explicación del concepto, el "aha moment" | Anécdotas irrelevantes |

Group consecutive segments if they form a coherent block (gap < 3 seconds).

Add 1 second padding before and after each segment for natural cuts:
```
actual_start = max(0, segment_start - 1)
actual_end = segment_end + 1
```

Present the selected highlights to the user before extracting, showing alignment to objective:
```
Objetivo: Instagram Reel (máx 60s)

Segmento 1: 00:12 → 00:18 (6s)  [GANCHO] — "Frase de apertura impactante"
Segmento 2: 02:10 → 02:35 (25s) [NÚCLEO] — "Punto más valioso del video"
Segmento 3: 08:44 → 09:05 (21s) [CIERRE] — "Llamada a acción clara"

Total: ~52s ✓ (dentro del límite de 60s)
```

Ask: "¿Procedo con la extracción? (puedes decirme qué cambiar)"

### Step E — Extract clips

For each highlight segment:

```bash
ffmpeg -i "<video_path>" \
  -ss <start> -to <end> \
  -c:v libx264 -c:a aac \
  -avoid_negative_ts make_zero \
  "<output_dir>/highlight_<N>_<start>s.mp4" -y
```

### Step F — Merge into reel (if requested)

Create a concat list:
```bash
# Generate file list
for clip in highlight_*.mp4; do echo "file '$clip'"; done > /tmp/concat_list.txt

# Merge
ffmpeg -f concat -safe 0 -i /tmp/concat_list.txt \
  -c:v libx264 -c:a aac \
  "<output_dir>/highlight_reel.mp4" -y
```

### Step G — Confirm output

```bash
ls -lh "<output_dir>"/highlight*.mp4
```

Show:
- List of files created
- Duration of each clip
- Total reel duration

---

## Output Directory Convention

Default: same folder as the input video, subfolder `highlights/`:
```
<video_dir>/highlights/
  highlight_1_12s.mp4
  highlight_2_130s.mp4
  highlight_reel.mp4
```

---

## Transcription Tips

| Situation | Recommendation |
|---|---|
| Video in English | Add `--language English` |
| Video in Spanish | Add `--language Spanish` |
| Mixed language | Omit `--language` |
| Long video (>30 min) | Use `faster-whisper` CLI for speed |
| Noisy audio | Use `medium` or `large` model |

### Using faster-whisper (alternative, faster)

```bash
pip install faster-whisper
python3 -c "
from faster_whisper import WhisperModel
model = WhisperModel('<model_size>', device='cpu', compute_type='int8')
segments, info = model.transcribe('/tmp/audio_extract.wav', beam_size=5)
for seg in segments:
    print(f'[{seg.start:.1f} --> {seg.end:.1f}] {seg.text}')
" > /tmp/transcript.txt
```

---

## Error Handling

| Error | Solution |
|---|---|
| `No such file` | Verify video path with `ls` |
| `ffmpeg: Unknown encoder` | Update ffmpeg: `brew upgrade ffmpeg` |
| `whisper: out of memory` | Use smaller model (`tiny` or `base`) |
| Empty transcription | Audio may be too quiet — check with `ffplay` |
| Segments overlap | Add `avoid_negative_ts make_zero` flag to ffmpeg |

---

## Anti-Patterns

- Don't extract clips without showing the user the selected segments first.
- Don't use `copy` codec when cutting mid-stream — use `libx264` to avoid black frames.
- Don't skip the padding (±1s) — hard cuts feel abrupt without it.
- Don't merge clips with different resolutions/fps without re-encoding.
