---
name: video-virality
description: Analyzes a video or its transcript and scores its viral potential for YouTube Shorts. Provides hook score, retention prediction, and specific improvement suggestions. Trigger with /video-virality.
intent: Takes a video file or transcript and evaluates it against YouTube Shorts virality signals — hook strength, pacing, emotional triggers, call to action, retention curve prediction — then delivers a scored report with actionable edits to maximize reach.
type: interactive
---

# Video Virality Analyzer

## Purpose

Score a video's viral potential for YouTube Shorts and deliver specific, actionable improvements. No generic advice — every suggestion is tied to a measurable signal.

## Prerequisites

```bash
which ffmpeg  || echo "MISSING: ffmpeg"
which whisper || echo "MISSING: whisper (pip install openai-whisper)"
```

## Interaction Flow

Ask **one question at a time**.

### Step 1 — Input

Ask:
> "¿Qué quieres analizar?
> 1. Un archivo de video (lo transcribo y analizo)
> 2. Una transcripción que ya tienes (pega el texto)
> 3. Solo el guion / script del video"

### Step 2 — Plataforma objetivo

Ask:
> "¿Para qué plataforma es el video?
> 1. YouTube Shorts ← default
> 2. TikTok
> 3. Instagram Reels
> 4. LinkedIn Video"

### Step 3 — Tipo de contenido

Ask:
> "¿Qué tipo de contenido es?
> 1. Tutorial / educativo
> 2. Opinión / punto de vista
> 3. Historia / narrativa
> 4. Demo de producto
> 5. Entretenimiento / humor
> 6. Motivacional"

---

## Execution Pipeline

### Step A — Transcribir (si es video)

```bash
ffmpeg -i "<video>" -vn -acodec pcm_s16le -ar 16000 -ac 1 /tmp/viral_audio.wav -y
whisper /tmp/viral_audio.wav --model small --output_format json --output_dir /tmp/viral_out
```

### Step B — Análisis de viralidad

Analiza el contenido contra los 8 factores de viralidad para Shorts:

---

## Los 8 Factores de Viralidad

### 1. Hook Score (0–10) — Primeros 3 segundos
El algoritmo de YouTube mide el % de usuarios que NO hacen scroll después del primer frame.

**Señales positivas:**
- Pregunta intrigante o afirmación contraintuitiva
- Promesa de valor concreta ("En 60 segundos vas a saber...")
- Conflicto, tensión o sorpresa inmediata
- Empieza IN MEDIAS RES — en medio de la acción

**Señales negativas:**
- "Hola, hoy voy a hablar de..." (-3 puntos)
- Introducción del speaker antes del gancho (-2 puntos)
- Silencio o música sola en los primeros 2s (-2 puntos)
- Logo/intro animada al inicio (-3 puntos)

### 2. Retention Curve (0–10) — Predicción de retención
Estima la curva de retención basándose en el ritmo del script.

**Calcular:**
- Contar cambios de tema/punto cada 10 segundos
- < 1 cambio cada 15s = riesgo de drop-off
- Pauses largas sin nuevo valor = pico de abandono

**Puntos de riesgo de abandono:**
- Segundos 3–8: si no hay payoff del hook
- Segundo 15–20: "valley of boring" — punto más peligroso
- Segundo 40–50: fatiga si el ritmo no varía

### 3. Emotional Triggers (0–10)
Cuántas emociones activa el contenido:

| Emoción | Efecto en viralidad |
|---|---|
| Sorpresa / "no sabía eso" | +3 shares |
| Validación / "yo también" | +3 saves |
| FOMO / urgencia | +2 clicks |
| Humor | +4 replay |
| Indignación moderada | +5 comentarios |
| Inspiración | +3 saves |

### 4. Value Density (0–10)
¿Cuánto valor por segundo entrega el video?

- Contar insights, datos, ejemplos o pasos concretos
- Dividir entre duración en segundos
- < 0.1 insights/seg = contenido diluido
- > 0.3 insights/seg = contenido denso (ideal para Shorts)

### 5. Call to Action Power (0–10)
¿El cierre motiva una acción concreta?

**CTAs que funcionan en Shorts:**
- "Guarda este video" (saves = señal de calidad para algoritmo)
- "Parte 2 si quieres saber..." (watch time en serie)
- "¿Estás de acuerdo? Comenta X o Y" (dicotomía fácil)
- Pregunta que genera debate en comentarios

**CTAs que NO funcionan:**
- "Dale like y suscríbete" (muy visto, ignorado)
- CTA sin contexto o motivación
- CTA después de los 55 segundos (ya terminó)

### 6. Pattern Interrupts (0–10)
¿Cuántas veces el contenido rompe expectativas o ritmo?

- Cambio de tono, velocidad o formato
- Dato inesperado
- Pausa dramática deliberada
- Cambio visual (si aplica)

Ideal: 1 pattern interrupt cada 10–15 segundos.

### 7. Shareability (0–10)
¿Quién lo compartiría y por qué?

- ¿Tiene un "punto de conversación" que la gente quiera mostrar a alguien?
- ¿Resuelve un problema que muchos tienen?
- ¿Dice algo que la gente quiere que otros escuchen?
- ¿Tiene un momento "screenshot-worthy" — frase memorable?

### 8. Algorithm Signals (0–10)
Factores técnicos que el algoritmo detecta:

| Factor | Peso |
|---|---|
| Duración 30–55s (sweet spot Shorts) | +2 |
| Audio claro, sin ruido | +1 |
| Subtítulos en el video | +2 |
| Primer frame visualmente atractivo | +1 |
| Velocidad de habla: 130–160 palabras/min | +1 |
| No redirige a link externo en el script | +1 |
| Termina antes de los 60s exactos | +2 |

---

## Output Format

Entregar un reporte estructurado:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ANÁLISIS DE VIRALIDAD — YouTube Shorts
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SCORE TOTAL: 67/100 ⚠️ Necesita ajustes

📌 Hook Score:        5/10  ← CRÍTICO
📈 Retention Curve:   7/10
💡 Emotional Triggers: 6/10
⚡ Value Density:     8/10
🎯 CTA Power:         4/10  ← MEJORAR
🔀 Pattern Interrupts: 6/10
📤 Shareability:      7/10
🤖 Algorithm Signals:  6/10

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  DIAGNÓSTICO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 CRÍTICO — Hook (5/10):
   El video empieza con "Hola, hoy quiero hablar de...".
   El 70% de los espectadores hace scroll en los primeros 2s.
   
   FIX: Reemplazar la apertura con:
   "El 90% de los videos de YouTube fallan por esto..."
   (intriga + dato + promesa de solución)

🟡 MEJORAR — CTA (4/10):
   "Dale like y suscríbete" es ignorado por el algoritmo.
   
   FIX: "Guarda este video — vas a necesitar esto"
   (saves son la señal de calidad #1 para Shorts en 2025)

🟢 MANTENER — Value Density (8/10):
   Excelente ritmo de información. No diluir.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  PREDICCIÓN DE RENDIMIENTO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Con el video actual:
  Retención promedio estimada: ~42%
  Probabilidad de boost algorítmico: baja

Con los fixes aplicados:
  Retención promedio estimada: ~61%
  Probabilidad de boost algorítmico: media-alta

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  PRÓXIMOS PASOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Regrabar los primeros 5 segundos con el nuevo hook
2. Cambiar CTA a "Guarda este video"
3. Agregar subtítulos quemados (/video-subtitles)
4. Re-analizar con /video-virality
```

---

## Score Ranges

| Score | Diagnóstico | Acción |
|---|---|---|
| 85–100 | 🟢 Alto potencial viral | Publicar |
| 70–84 | 🟡 Buen potencial | 1–2 ajustes menores |
| 55–69 | 🟠 Potencial medio | Refactorizar hook y CTA |
| 40–54 | 🔴 Bajo potencial | Restructurar contenido |
| < 40 | ⛔ Muy bajo | Replantear desde el guion |

---

## Anti-Patterns

- No dar scores sin explicar exactamente qué los baja.
- No recomendar "más calidad" o "mejor edición" — ser específico con timestamps y frases.
- No comparar con otros creadores sin datos concretos.
- Siempre ofrecer un fix de texto específico, no solo diagnóstico.
