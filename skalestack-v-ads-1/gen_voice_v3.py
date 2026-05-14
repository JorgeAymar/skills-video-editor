#!/usr/bin/env python3
"""
gen_voice_v3.py — v-ads-1
Genera audio TTS + SRT con guion honesto, posicionamiento high-ticket.
"""
import os, json, subprocess, wave, struct
from pathlib import Path

BASE  = "/Users/jorgesaymar/Desktop/Video-editor-test/skalestack-v-ads-1"
TMP   = "/tmp/skalestack_v3"
SPEAKER = f"{BASE}/audio/voice_v2_dionisio.wav"
MUSIC   = f"{BASE}/audio/music_beyond.mp3"  # AShamaluevMusic "Beyond" — cinematic dark

os.makedirs(TMP, exist_ok=True)

# ── Guion HIGH-TICKET v3 ─────────────────────────────────────────────────────
SEGMENTS = [
    # (id, texto_voz) — Guion v4: honesto, enfocado en servicio, sin promesas falsas
    (0, "Si ya gastaste en marketing y el número no se mueve, el problema no es el presupuesto."),
    (1, "La mayoría de fundadores sigue comprando más tráfico. Los que escalan construyen su sistema de crecimiento."),
    (2, "Growth Hacking es un sistema de experimentos, datos y velocidad, diseñado para tu negocio."),
    (3, "En SkaleStack construimos tu sistema de Growth Hacking desde cero. Experimentamos rápido, medimos todo, y escalamos lo que funciona."),
    (4, "No trabajamos con todos. Solo con startups B2B comprometidas a construir crecimiento real con método."),
    (5, "¿Tu empresa califica? Agenda tu sesión estratégica en skalestack punto com."),
]

GAP_S   = 0.20   # silencio entre segmentos
ATEMPO  = 1.4    # velocidad de locución
SR      = 44100

def wav_duration(path):
    with wave.open(path, 'r') as f:
        return f.getnframes() / f.getframerate()

def gen_silence(duration_s, path):
    n = int(SR * duration_s)
    with wave.open(path, 'w') as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR)
        f.writeframes(struct.pack('<' + 'h'*n, *([0]*n)))

def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        print(f"ERROR: {' '.join(cmd[:3])}")
        print(r.stderr[-300:])
        raise RuntimeError("subprocess failed")
    return r

# ── Step 1: Generate raw TTS segments ────────────────────────────────────────
print("="*60)
print("  Gen Voice v3 — Guion High-Ticket")
print("="*60)
print("\n[1/5] Generando voz XTTS-v2...")

from TTS.api import TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")

raw_paths = []
for idx, text in SEGMENTS:
    out = f"{TMP}/seg_{idx}_raw.wav"
    print(f"  Seg {idx}: {text[:60]}...")
    tts.tts_to_file(text=text, speaker_wav=SPEAKER, language="es", file_path=out)
    raw_paths.append(out)

# ── Step 2: Speed up to 1.4x + resample 44100Hz mono ─────────────────────────
print("\n[2/5] Aplicando atempo 1.4x...")
fast_paths = []
for idx, raw in enumerate(raw_paths):
    fast = f"{TMP}/seg_{idx}_fast.wav"
    run(["ffmpeg", "-y", "-i", raw,
         "-af", f"atempo={ATEMPO}",
         "-ar", str(SR), "-ac", "1", fast])
    dur = wav_duration(fast)
    print(f"  seg_{idx}: {dur:.3f}s")
    fast_paths.append((fast, dur))

# ── Step 3: Build concat list with silence gaps ───────────────────────────────
print("\n[3/5] Concatenando con gaps 0.2s...")
concat_files = []
for i, (fp, dur) in enumerate(fast_paths):
    concat_files.append(fp)
    if i < len(fast_paths) - 1:
        sil = f"{TMP}/sil_{i}.wav"
        gen_silence(GAP_S, sil)
        concat_files.append(sil)

concat_list = f"{TMP}/concat_v3.txt"
with open(concat_list, "w") as f:
    for p in concat_files:
        f.write(f"file '{p}'\n")

voice_raw = f"{TMP}/voice_v3.wav"
run(["ffmpeg", "-y", "-f", "concat", "-safe", "0",
     "-i", concat_list, "-ar", str(SR), "-ac", "1", voice_raw])

total_voice = wav_duration(voice_raw)
print(f"  Voz total: {total_voice:.3f}s")

# ── Step 4: SRT generation ────────────────────────────────────────────────────
print("\n[4/5] Generando SRT...")
durations = [d for _, d in fast_paths]
total_with_gaps = total_voice

srt_path = f"{TMP}/skalestack_v3.srt"
cursor = 0.0
srt_lines = []
for i, (text, dur) in enumerate(zip([s[1] for s in SEGMENTS], durations)):
    start = cursor + 0.200  # 200ms lead-in gap on first seg
    if i == 0:
        start = cursor
    end = start + dur
    def fmt(t):
        h=int(t//3600); m=int((t%3600)//60); s=int(t%60); ms=int((t%1)*1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
    srt_lines.append(f"{i+1}\n{fmt(start)} --> {fmt(end)}\n{text}\n")
    cursor = end + GAP_S

with open(srt_path, "w") as f:
    f.write("\n".join(srt_lines))
print(f"  SRT: {srt_path}")

# Save durations JSON for render script
total_padded = total_with_gaps + 3.5  # 3.5s CTA hold after voice
durations_data = {
    "durations_fast": durations,
    "total": total_with_gaps,
    "total_padded": total_padded,
    "gap": GAP_S
}
with open(f"{TMP}/durations_v3.json", "w") as f:
    json.dump(durations_data, f, indent=2)
print(f"  Duración total: {total_with_gaps:.3f}s  (+3.5s pad = {total_padded:.3f}s)")

# ── Step 5: Mix audio (voice + padded silence + music) ───────────────────────
print("\n[5/5] Mezclando audio...")
voice_padded = f"{TMP}/voice_v3_padded.wav"
run(["ffmpeg", "-y", "-i", voice_raw,
     "-af", f"apad=whole_dur={total_padded}",
     "-ar", str(SR), "-ac", "2", voice_padded])

audio_out = f"{TMP}/audio_v3_ht.wav"
run(["ffmpeg", "-y",
     "-i", voice_padded,
     "-i", MUSIC,
     "-filter_complex",
     f"[1:a]atrim=0:{total_padded+2},asetpts=PTS-STARTPTS[mt];"
     f"[mt]afade=t=in:st=0:d=0.5[mfi];"
     f"[mfi]afade=t=out:st={total_padded-1.5}:d=2.0[mfo];"
     f"[mfo]volume=0.55[music];"
     f"[0:a][music]amix=inputs=2:duration=first:normalize=0[out]",
     "-map", "[out]", "-ar", "44100", "-ac", "2", audio_out])

# QA
r = subprocess.run(["ffmpeg", "-i", audio_out, "-af", "volumedetect", "-f", "null", "/dev/null"],
                   capture_output=True, text=True)
for l in r.stderr.splitlines():
    if "mean_volume" in l or "max_volume" in l:
        print(f"  {l.strip()}")

print(f"\n{'='*60}")
print(f"  Audio listo → {audio_out}")
print(f"  SRT listo   → {srt_path}")
print(f"  Total       : {total_padded:.3f}s  ({int(total_padded*30)} frames @ 30fps)")
print(f"{'='*60}")
