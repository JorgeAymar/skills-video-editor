# PLAN DE PRODUCCIÓN VIDEO ADS — v-ads-1
**Fecha:** 2026-05-13 | **Plataforma:** Instagram Ads (Reels) | **Estado:** RE-RENDER PENDIENTE — TTS guion nuevo

---


## ESTADO DE ASSETS

| Asset | Archivo | Estado |
|---|---|---|
| Voz mezclada (VIGENTE) | `/tmp/skalestack_v3/audio_v3_ht.wav` — 36.382s (guion v3, TEMPORAL) | ⚠️ REEMPLAZAR |
| **Voz nueva** | Regenerar con `gen_voice_v3.py` | ⏳ PENDIENTE |
| **Música nueva** | `audio/music_beyond.mp3` — 205s, cinematic dark (AShamaluevMusic) | ✅ LISTO |
| Música candidata B | `audio/music_strength.mp3` — 194s | ✅ LISTO |
| Música candidata C | `audio/music_foundation.mp3` — 196s | ✅ LISTO |
| SRT vigente (TEMPORAL) | `/tmp/skalestack_v3/skalestack_v3.srt` — temporal | ⚠️ REEMPLAZAR |
| Clip 1 | `stock/new_clip1_money_loss.mp4` — vertical 9:16 | ✅ LISTO |
| Clip 2 | `stock/new_clip2_dark_laptop.mp4` — vertical 9:16 | ✅ LISTO |
| Clip 3 | `stock/new_clip3_analytics.mp4` — vertical 9:16 | ✅ LISTO |
| Clip 4 | `stock/new_clip4_man_camera.mp4` — vertical 9:16 | ✅ LISTO |
| Clip 5 | `stock/new_clip5_confident.mp4` — vertical 9:16 | ✅ LISTO |

---

## 1. ESPECIFICACIONES TÉCNICAS

```
Resolución salida:  1080 x 1920 px (9:16 vertical — Instagram Ads Reels)
FPS:                30
Codec video:        libx264, preset fast, crf 22
Codec audio:        aac, 128k
Sample rate audio:  44100 Hz, stereo
Duración estimada:  ~34–38s (se confirma tras regenerar TTS)
Plataforma:         Instagram Ads — Reels
Límite duración:    60s max ✅ (~38s estimado)
Límite archivo:     4 GB max ✅ (~7 MB actual)
Safe zone texto:    evitar 14% superior e inferior (UI de Instagram)
```

---

## 2. GUION EXACTO — VOZ + PANTALLA

> **Principio:** Solo comunicar lo que el servicio realmente hace.
> Sin métricas inventadas. Sin garantías de "gratis". Posicionamiento por método y exclusividad.

| # | Escena | VOZ (audio) | H1 (texto exacto · fuente · tamaño · color · animación) | H2 (texto exacto · fuente · tamaño · color · animación) |
|---|---|---|---|---|
| 1 | HOOK — Dolor calificado | "Si ya gastaste en marketing y el número no se mueve, el problema no es el presupuesto." | **"EL PROBLEMA"** · Arial Bold · 88px · #FFFFFF Blanco · typewriter | *"No es el presupuesto."* · Arial Regular · 60px · #FF3B3B Rojo · punch-in |
| 2 | PROBLEMA — Los que escalan | "La mayoría de fundadores sigue comprando más tráfico. Los que escalan construyen su sistema de crecimiento." | **"MÁS TRÁFICO."** · Arial Bold · 88px · #FFFFFF Blanco · punch-in | *"No convierte."* · Arial Bold · 56px · #FF3B3B Rojo · punch-in |
| 3 | SOLUCIÓN — El sistema | "Growth Hacking es un sistema de experimentos, datos y velocidad, diseñado para tu negocio." | **"EXPERIMENTOS."** · Arial Bold · 88px · #00FF88 Verde · punch-in | *"Datos. Velocidad."* · Arial Bold · 56px · #FFFFFF Blanco · punch-in |
| 4 | MARCA — Qué hace SkaleStack | "En SkaleStack construimos tu sistema de Growth Hacking desde cero. Experimentamos rápido, medimos todo, y escalamos lo que funciona." | **"SkaleStack.com"** · Arial Bold · 96px · #FFFFFF Blanco · punch-in | *"Experimenta. Mide. Escala."* · Arial Bold · 52px · #00FF88 Verde · punch-in |
| 5 | EXCLUSIVIDAD — No para todos | "No trabajamos con todos. Solo con startups B2B comprometidas a construir crecimiento real con método." | **"EXCLUSIVO."** · Arial Bold · 96px · #00FF88 Verde · punch-in | *"Solo startups B2B."* · Arial Bold · 56px · #FFFFFF Blanco · punch-in |
| 6 | CTA — Calificador | "¿Tu empresa califica? Agenda tu sesión estratégica en skalestack punto com." | **"¿CALIFICAS?"** · Arial Bold · 96px · #00FF88 Verde · punch-in | **"SkaleStack.com"** · Arial Bold · 72px · #FFFFFF Blanco · punch-in |

### Por qué este guion es profesional y honesto

| Señal | Antes | Ahora |
|---|---|---|
| Métricas | "3.2x conversión" (no verificable) | Sin métricas — el servicio habla por sí mismo |
| Garantía | "no cobramos" (implica gratis) | "No trabajamos con todos" (exclusividad) |
| CTA | "Sesión estratégica" ✓ | "Sesión estratégica" ✓ |
| Mensaje central | Resultados numéricos | Metodología + proceso + calificación |
| Posicionamiento | Promesas | Autoridad y método |

---

## 3. JERARQUÍA VISUAL — REGLAS POR ESCENA

> **Regla de oro:** Máximo 2 elementos de texto por escena (H1 + H2).
> H1 domina. H2 contrasta en color Y tamaño (mínimo 24px de diferencia).
> Un solo color por función: Blanco = autoridad, Verde = beneficio/CTA, Rojo = dolor/problema.
> Sin líneas decorativas. Sin H3. Sin subrayados.

### ESCENA 1 — HOOK
```
H1: "EL PROBLEMA"            → Arial Bold 88px, #FFFFFF BLANCO — typewriter (frame 3, 6f)
H2: "No es el presupuesto."  → Arial Regular 60px, #FF3B3B ROJO — punch-in (frame 14, 8f)
Stroke: 2px negro en ambos
Posición: H1 y=820px, H2 y=970px
Diferencia de tamaño: 28px ✅
```

### ESCENA 2 — PROBLEMA
```
H1: "MÁS TRÁFICO."   → Arial Bold 88px, #FFFFFF BLANCO — punch-in (frame 130, 6f)
H2: "No convierte."  → Arial Bold 56px, #FF3B3B ROJO — punch-in (frame 143, 8f)
Stroke: 2px negro en ambos
Posición: H1 y=820px, H2 y=970px
Diferencia de tamaño: 32px ✅
```

### ESCENA 3 — SOLUCIÓN
```
H1: "EXPERIMENTOS."      → Arial Bold 88px, #00FF88 VERDE — punch-in (frame 337, 5f)
H2: "Datos. Velocidad."  → Arial Bold 56px, #FFFFFF BLANCO — punch-in (frame 355, 6f)
Stroke: 2px negro en ambos
Posición: H1 y=820px, H2 y=970px
Diferencia de tamaño: 32px ✅
```

### ESCENA 4 — MARCA
```
H1: "SkaleStack.com"             → Arial Bold 96px, #FFFFFF BLANCO — punch-in (frame 492, 8f)
H2: "Experimenta. Mide. Escala." → Arial Bold 52px, #00FF88 VERDE — punch-in (frame 510, 6f)
Stroke: 2px negro en ambos
Posición: H1 y=820px, H2 y=970px
Diferencia de tamaño: 44px ✅
```

### ESCENA 5 — EXCLUSIVIDAD
```
H1: "EXCLUSIVO."         → Arial Bold 96px, #00FF88 VERDE — punch-in (frame 727, 6f)
H2: "Solo startups B2B." → Arial Bold 56px, #FFFFFF BLANCO — punch-in (frame 742, 8f)
Stroke: 2px negro en ambos
Posición: H1 y=820px, H2 y=970px
Diferencia de tamaño: 40px ✅
```

### ESCENA 6 — CTA
```
H1: "¿CALIFICAS?"    → Arial Bold 96px, #00FF88 VERDE — punch-in (frame 904, 5f)
H2: "SkaleStack.com" → Arial Bold 72px, #FFFFFF BLANCO — punch-in (frame 920, 6f)
Stroke: 2px negro en ambos
Posición: H1 y=820px, H2 y=980px
Diferencia de tamaño: 24px ✅
```

---

## 4. PALETA Y TIPOGRAFÍA

```
COLORES
  Fondo base:        #0D0D0D  (RGB 13,13,13)
  Verde marca:       #00FF88  (RGB 0,255,136) — beneficios, CTA, elementos positivos
  Blanco principal:  #FFFFFF  — statements de autoridad, H1
  Gris secundario:   #969696  — descriptores, información de apoyo
  Rojo acento:       #FF3B3B  — dolor, problema (solo escenas 1 y 2)
  NUNCA: amarillo, naranja, azul — rompen la paleta de marca

FUENTES (rutas absolutas macOS)
  Bold:    /System/Library/Fonts/Supplemental/Arial Bold.ttf
  Regular: /System/Library/Fonts/Supplemental/Arial.ttf

JERARQUÍA DE TAMAÑOS
  H1 dominante:   88–96px (solo UNO por escena)
  H2 contraste:   52–64px (mínimo 24px más pequeño que H1)
  Logo firma:     32px (top-left, discreta)
  Subtítulo:      78px (zona inferior, independiente de los textos de escena)

STROKE (contorno de texto)
  Todos los textos de escena llevan stroke negro de 2px
  Propósito: legibilidad sobre clips con fondos claros o variados
  Implementación: stroke_width=2, stroke_fill=(0,0,0,200) en PIL ImageDraw.text()
  Subtítulos: sin stroke (ya tienen fondo redondeado negro)

REGLA MÁXIMA: solo H1 + H2 por escena. Sin H3, sin líneas decorativas, sin subrayados.
```

---

## 5. STACK DE CAPAS

```
CAPA 6 — SUBTÍTULO KARAOKE
  Fuente:     Bold 78px, #FFFFFF
  Posición:   y=1660px (86% de 1920)
  Fondo:      rounded rect negro alpha=210, radius=18
  Chunks:     máx 18 chars — sin guiones "—" (se limpian en display)
  Fade:       in 3 frames / out 2 frames

CAPA 5 — TEXTOS ANIMADOS (según jerarquía por escena — ver sección 3)

CAPA 4 — LOGO FIRMA (persistente)
  Texto:      "SkaleStack.com"
  Fuente:     Arial Bold 32px, #FFFFFF, alpha máx 180
  Posición:   x=48px, y=120px (top-left)
  Línea:      #00FF88, 2px, 80px ancho, y=162px

CAPA 3 — TINT + OVERLAY
  (ver sección 7)

CAPA 2 — BARRA DE PROGRESO
  Color:  #00FF88, y=H-77 a H-73, crece con f/1090*W

CAPA 1 — VIDEO STOCK + KEN BURNS
```

---

## 6. LÍNEA DE TIEMPO (timings a confirmar tras nuevo TTS)

```
ESCENA   FRAMES      DURACIÓN   CLIP                    TRANSICIÓN
──────────────────────────────────────────────────────────────────────
1-HOOK   0→128       4.27s      new_clip1_money_loss    → whip right f118-139
2-PROB   140→329     6.33s      new_clip2_dark_laptop   → flash blanco f315-340
3-SOL    341→521     6.03s      new_clip3_analytics     → zoom punch f507-532
4-MARCA  533→785     8.43s      new_clip4_man_camera    → wipe up f771-796
5-EXCL   797→859     2.10s      new_clip5_confident     → fade black f845-870
6-CTA    871→1090    7.33s      negro sólido            → fade black f1061-1090
TOTAL    1091 frames 36.37s
```
⚠️ Estos timings son del render anterior. Cambiarán al regenerar TTS con el guion actual.

---

## 7. OVERLAY ALPHA + TINT POR ESCENA

| Escena | Alpha | Tint BGR | Propósito emocional |
|---|---|---|---|
| 1 — Hook | 140 | ×1.05, ×0.88, ×0.85 (azul frío) | Dolor — distancia emocional |
| 2 — Problema | 153 | ×1.02, ×0.88, ×0.88 (frío desaturado) | Frustración — más oscuro |
| 3 — Solución | 128 | ×0.88, ×1.05, ×0.90 (verde energía) | Esperanza — el sistema |
| 4 — Marca | 166 | ×0.92, ×1.02, ×0.96 (neutral) | Autoridad — texto protagonista |
| 5 — Exclusividad | 140 | ×0.86, ×1.08, ×0.88 (verde intenso) | Credibilidad — resultado |
| 6 — CTA | 255 | neutral | Negro puro — máximo contraste |

---

## 8. MÚSICA

```
Pista seleccionada: music_beyond.mp3 (AShamaluevMusic "Beyond")
Duración:           205s (más que suficiente para 36s de video)
Licencia:           Free para uso comercial (AShamaluevMusic)
Volumen mezcla:     0.55 (amix normalize=0)
Fade in música:     0.5s al inicio
Fade out música:    1.5s antes del fin

Candidatas alternativas:
  - music_strength.mp3 (194s) — más corporativo/power
  - music_foundation.mp3 (196s) — más contemplativo/building

Confirmada: music_beyond.mp3 ✅
```

---

## 9. SINCRONIZACIÓN AUDIO

| Seg | Texto VOZ | Duración estimada post-1.4x |
|---|---|---|
| 0 | "Si ya gastaste en marketing y el número no se mueve, el problema no es el presupuesto." | ~4.0s |
| 1 | "La mayoría de fundadores sigue comprando más tráfico. Los que escalan construyen su sistema de crecimiento." | ~5.8s |
| 2 | "Growth Hacking es un sistema de experimentos, datos y velocidad, diseñado para tu negocio." | ~5.5s |
| 3 | "En SkaleStack construimos tu sistema de Growth Hacking desde cero. Experimentamos rápido, medimos todo, y escalamos lo que funciona." | ~8.0s |
| 4 | "No trabajamos con todos. Solo con startups B2B comprometidas a construir crecimiento real con método." | ~6.5s |
| 5 | "¿Tu empresa califica? Agenda tu sesión estratégica en skalestack punto com." | ~4.5s |

**Total estimado:** ~34.3s + 0.2s × 5 gaps + 3.5s tail ≈ **~38.8s**
⚠️ Duraciones exactas se determinan al correr gen_voice_v3.py

---

## 10. SUBTÍTULOS

```
Archivo SRT:   /tmp/skalestack_v3/skalestack_v3.srt (regenerar con nuevo TTS)
Modo:          Karaoke — chunks máx 18 chars
Posición:      y=1660px
Fuente:        Bold 78px, #FFFFFF
Limpieza:      em-dashes "—" se limpian en draw_subtitle() antes de mostrar
Fondo:         rounded rect negro alpha=210, radius=18, padding 28/14px
```

---

## 11. ORDEN DE EJECUCIÓN

```
PASO  ESTADO              ACCIÓN
──────────────────────────────────────────────────────────────────────
1     ✅ COMPLETADO       Guion honesto definido
2     ✅ COMPLETADO       Visual hierarchy corregida en render_v4.py
3     ✅ COMPLETADO       Logo → "skalestack.com"
4     ✅ COMPLETADO       Dashes limpiados en draw_subtitle()
5     ✅ COMPLETADO       Música cinematic descargada (Beyond, Strength, Foundation)
6     ✅ COMPLETADO       gen_voice_v3.py actualizado con guion honesto + nueva música
7     ✅ COMPLETADO       Música confirmada — music_beyond.mp3
8     ⏳ PENDIENTE        Ejecutar gen_voice_v3.py → nuevo audio + SRT
9     ⏳ PENDIENTE        Actualizar SCENES[] en render_v4.py con nuevos timings
10    ⏳ PENDIENTE        Render final → v-ads-1.mp4
11    ⏳ PENDIENTE        Gate visual — revisar jerarquía, música, subtítulos
12    ⏳ PENDIENTE        Gate técnico — /video-qa
13    ⏳ PENDIENTE        Aprobación final del usuario
```

---

## 12. GATES DE CALIDAD

### Gate visual (reproducir v-ads-1.mp4)

**Jerarquía visual**
- [ ] Cada escena tiene UN elemento dominante claro (H1 grande)
- [ ] H2 es visiblemente más pequeño que H1 (mínimo 20px diferencia)
- [ ] No más de 3 elementos de texto por escena
- [ ] Sin textos redundantes con el subtítulo

**Logo y branding**
- [ ] Logo dice "skalestack.com" (no "SkaleStack")
- [ ] Logo visible pero no compite con texto principal
- [ ] "skalestack.com" se muestra >4s en escena 6

**Subtítulos**
- [ ] Sin guiones "—" en los chunks karaoke
- [ ] Chunks pequeños (2–4 palabras), no líneas completas
- [ ] Sincronizados con la voz

**Contenido honesto**
- [ ] Sin "3.2x conversión" ni ninguna métrica inventada
- [ ] Sin "no cobramos" ni ninguna promesa de gratis
- [ ] Escena 4 habla del servicio (Growth Hacking), no de resultados numéricos
- [ ] Escena 5 usa exclusividad, no garantía financiera

**Audio**
- [ ] Música dark cinematic — encaja con servicio high-ticket
- [ ] Voz audible sobre la música
- [ ] Sin cortes abruptos de audio

### Gate técnico
```bash
ffprobe -v quiet -show_entries format=duration,size \
  -show_entries stream=codec_name,width,height,r_frame_rate \
  -of default output/v-ads-1.mp4

# Criterios:
# ✅ 1080x1920 (9:16)
# ✅ 30fps, h264, aac
# ✅ Duración 34–40s
# ✅ mean_volume entre -25 y -10 dBFS
```

---

## 13. RUTAS DE ARCHIVOS

```
BASE:  /Users/jorgesaymar/Desktop/Video-editor-test/skalestack-v-ads-1/

CLIPS (verticales 9:16):
  stock/new_clip1_money_loss.mp4    (Pexels 6282378)
  stock/new_clip2_dark_laptop.mp4   (Pexels 5495895)
  stock/new_clip3_analytics.mp4     (Pexels 7947438)
  stock/new_clip4_man_camera.mp4    (Pexels 3713695)
  stock/new_clip5_confident.mp4     (Pexels 8348913)

AUDIO:
  audio/voice_v2_dionisio.wav       (speaker reference XTTS-v2 — no cambiar)
  audio/music_beyond.mp3            (pista seleccionada — 205s cinematic dark)
  audio/music_strength.mp3          (alternativa A)
  audio/music_foundation.mp3        (alternativa B)

GENERADOS en /tmp/skalestack_v3/:
  audio_v3_ht.wav                   (⚠️ temporal — del guion v3, reemplazar)
  skalestack_v3.srt                 (⚠️ temporal — del guion v3, reemplazar)

SALIDA:
  output/v-ads-1.mp4                ← DESTINO DEL PRÓXIMO RENDER
```

---

**REGLA DE ORO:**
Un video profesional tiene jerarquía visual clara, contenido honesto, y música que refuerza la emoción.
Antes de renderizar: todos los assets confirmados. No se avanza sin el guion de voz aprobado.
