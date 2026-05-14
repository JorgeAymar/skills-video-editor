#!/usr/bin/env python3
"""
render_v4.py — v-ads-1 (EMOCIÓN: Ken Burns, shake, whip, tints)
"""
import cv2, numpy as np, subprocess, sys, re, os, math
from PIL import Image, ImageDraw, ImageFont

BASE  = "/Users/jorgesaymar/Desktop/Video-editor-test/skalestack-v-ads-1"
TMP   = "/tmp/skalestack_v3"
CLIPS = {
    1: f"{BASE}/stock/new_clip1_money_loss.mp4",      # animación pérdida de dinero — hook
    2: f"{BASE}/stock/new_clip2_dark_laptop.mp4",     # hombre laptop cuarto oscuro — dolor
    3: f"{BASE}/stock/new_clip3_analytics.mp4",       # analytics / datos — solución
    4: f"{BASE}/stock/new_clip4_man_camera.mp4",      # hombre barbado mirando cámara — marca
    5: f"{BASE}/stock/new_clip5_confident.mp4",       # hombre traje mirando cámara — resultado
}
VOICE_PADDED = f"{TMP}/voice_padded.wav"
AUDIO_OUT    = f"/tmp/skalestack_v3/audio_v3_ht.wav"
VIDEO_RAW    = f"{BASE}/output/v-ads-1_raw.mp4"
VIDEO_OUT    = f"{BASE}/output/v-ads-1.mp4"
SRT_PATH     = f"/tmp/skalestack_v3/skalestack_v3.srt"

W, H, FPS, TOTAL = 1080, 1920, 30, 1208
CX = W // 2

BLACK_BG = (13,13,13)
WHITE    = (255,255,255,255)
GREEN    = (0,255,136,255)
RED_ACC  = (255,59,59,255)
GRAY_ACC = (170,170,170,255)

BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
REG  = "/System/Library/Fonts/Supplemental/Arial.ttf"

def fnt(path, size):
    try:    return ImageFont.truetype(path, size)
    except: return ImageFont.load_default()

F_LOGO = fnt(BOLD, 38);  F_T96 = fnt(BOLD, 96);  F_T88 = fnt(BOLD, 88)
F_T76  = fnt(BOLD, 76);  F_T72 = fnt(BOLD, 72);  F_T56 = fnt(BOLD, 56)
F_T52  = fnt(REG,  52);  F_T44 = fnt(REG,  44);  F_T36 = fnt(REG,  36)
F_SUB  = fnt(BOLD, 78)

# ── SRT ───────────────────────────────────────────────────────────────────────
def parse_srt(path):
    segs = []
    blocks = re.split(r"\n\n+", open(path).read().strip())
    for b in blocks:
        ls = b.strip().splitlines()
        if len(ls) < 3: continue
        m = re.match(r"(\d+):(\d+):(\d+),(\d+) --> (\d+):(\d+):(\d+),(\d+)", ls[1])
        if not m: continue
        def ts(*g): return int(g[0])*3600+int(g[1])*60+int(g[2])+int(g[3])/1000
        segs.append({"start": ts(*m.groups()[:4]), "end": ts(*m.groups()[4:]), "text": " ".join(ls[2:])})
    return segs

def expand_to_chunks(srt, max_chars=18):
    """Split each SRT segment into small chunks — TikTok karaoke style."""
    chunks = []
    for seg in srt:
        words = seg["text"].split()
        groups, group = [], []
        for w in words:
            group.append(w)
            if len(" ".join(group)) >= max_chars:
                groups.append(" ".join(group))
                group = []
        if group:
            groups.append(" ".join(group))
        n = len(groups)
        dur = (seg["end"] - seg["start"]) / max(1, n)
        for i, g in enumerate(groups):
            chunks.append({
                "start": seg["start"] + i * dur,
                "end":   seg["start"] + (i + 1) * dur,
                "text":  g,
            })
    return chunks

SRT = expand_to_chunks(parse_srt(SRT_PATH), max_chars=18)

def srt_at(t):
    for s in SRT:
        if s["start"] <= t <= s["end"]: return s
    return None

# ── Scenes ────────────────────────────────────────────────────────────────────
SCENES = [
    {"id":1,"clip":1,"f0":0,  "f1":120, "alpha":140},
    {"id":2,"clip":2,"f0":127,"f1":327, "alpha":153},
    {"id":3,"clip":3,"f0":334,"f1":482, "alpha":128},
    {"id":4,"clip":4,"f0":489,"f1":717, "alpha":166},
    {"id":5,"clip":5,"f0":724,"f1":894, "alpha":140},
    {"id":6,"clip":0,"f0":901,"f1":1207,"alpha":255},
]

def scene_at(f):
    for s in SCENES:
        if s["f0"] <= f <= s["f1"]: return s
    for i,s in enumerate(SCENES[:-1]):
        if s["f1"] < f < SCENES[i+1]["f0"]: return s
    return SCENES[-1]

_caps, _fcounts = {}, {}

def get_bg(clip_id, f, scene):
    if clip_id == 0:
        bg = np.zeros((H,W,3), np.uint8); bg[:] = BLACK_BG; return bg
    if clip_id not in _caps:
        _caps[clip_id] = cv2.VideoCapture(CLIPS[clip_id])
        _fcounts[clip_id] = int(_caps[clip_id].get(cv2.CAP_PROP_FRAME_COUNT))
    cap = _caps[clip_id]
    local = (f - scene["f0"]) % max(1, _fcounts[clip_id])
    cap.set(cv2.CAP_PROP_POS_FRAMES, local)
    ret, fr = cap.read()
    if not ret: cap.set(cv2.CAP_PROP_POS_FRAMES,0); ret,fr = cap.read()
    if not ret: return np.zeros((H,W,3), np.uint8)
    return fr

def crop916(fr):
    h,w = fr.shape[:2]
    nw = int(h*9/16)
    if nw > w: nh = int(w*16/9); y=(h-nh)//2; fr=fr[y:y+nh,:]
    else: x=(w-nw)//2; fr=fr[:,x:x+nw]
    return cv2.resize(fr,(W,H),interpolation=cv2.INTER_LINEAR)

def darken(fr, alpha):
    if alpha==0: return fr
    return cv2.addWeighted(fr, 1-alpha/255.0, np.zeros_like(fr), alpha/255.0, 0)

# ── Ken Burns: slow zoom per scene (makes footage feel alive) ─────────────────
def ken_burns(fr, f, scene):
    f0, f1 = scene["f0"], scene["f1"]
    sid = scene["id"]
    duration = max(1, f1 - f0)
    p = (f - f0) / duration
    # Alternate: odd scenes zoom in, even scenes zoom out
    if sid % 2 == 1:
        scale = 1.0 + 0.06 * p        # 1.00 → 1.06
    else:
        scale = 1.06 - 0.06 * p       # 1.06 → 1.00
    if abs(scale - 1.0) < 0.001: return fr
    h, w = fr.shape[:2]
    M = cv2.getRotationMatrix2D((w/2, h/2), 0, scale)
    return cv2.warpAffine(fr, M, (w, h))

# ── Color tint per scene: BGR multipliers ─────────────────────────────────────
TINTS = {
    1: (1.05, 0.88, 0.85),   # cold blue: problem/pain
    2: (1.02, 0.88, 0.88),   # desaturated cold: more pain
    3: (0.88, 1.05, 0.90),   # green tint: solution energía
    4: (0.92, 1.02, 0.96),   # neutral warm: brand reveal
    5: (0.86, 1.08, 0.88),   # strong green: results
    6: (1.0,  1.0,  1.0),    # neutral: CTA
}

def apply_tint(fr, sid):
    b, g, r = TINTS.get(sid, (1,1,1))
    out = fr.astype(np.float32)
    out[:,:,0] = np.clip(out[:,:,0]*b, 0, 255)
    out[:,:,1] = np.clip(out[:,:,1]*g, 0, 255)
    out[:,:,2] = np.clip(out[:,:,2]*r, 0, 255)
    return out.astype(np.uint8)

# ── Screen shake (used for hook reveal) ───────────────────────────────────────
def shake_offset(f, trigger_f, duration=15, magnitude=10):
    local = f - trigger_f
    if local < 0 or local >= duration: return 0, 0
    decay = (1 - local/duration)**2 * magnitude
    dx = int(decay * math.sin(local * 2.2))
    dy = int(decay * math.cos(local * 3.1) * 0.5)
    return dx, dy

def apply_shake(fr, dx, dy):
    if dx==0 and dy==0: return fr
    M = np.float32([[1,0,dx],[0,1,dy]])
    return cv2.warpAffine(fr, M, (W,H), borderMode=cv2.BORDER_REPLICATE)

# ── Easing / animation helpers ────────────────────────────────────────────────
def eoc(t): return 1-(1-max(0.,min(1.,t)))**3
def eio(t): t=max(0.,min(1.,t)); return 4*t*t*t if t<0.5 else 1-(-2*t+2)**3/2
def prog(f,f0,dur): return min(1., max(0., (f-f0)/max(1,dur)))

def tw_alpha(img, text, fnt, cx, y, color_rgb, alpha):
    if alpha<=0 or not text: return
    d0 = ImageDraw.Draw(Image.new("RGBA",(1,1)))
    bb = d0.textbbox((0,0), text, font=fnt)
    w = bb[2]-bb[0]
    o = Image.new("RGBA", img.size, (0,0,0,0))
    ImageDraw.Draw(o).text(
        (cx-w//2, y), text, font=fnt,
        fill=color_rgb[:3]+(int(alpha),),
        stroke_width=2, stroke_fill=(0,0,0,int(alpha*0.8))
    )
    img.alpha_composite(o)

def slide_up(img, text, fnt, cx, y, p, color, off=50):
    ease = eoc(p); y2 = int(y + off*(1-ease)); a = int(255*min(1.,p*4))
    tw_alpha(img, text, fnt, cx, y2, color, a)

def slide_down(img, text, fnt, cx, y, p, color, off=50):
    ease = eoc(p); y2 = int(y - off*(1-ease)); a = int(255*min(1.,p*4))
    tw_alpha(img, text, fnt, cx, y2, color, a)

def fade_in(img, text, fnt, cx, y, p, color):
    tw_alpha(img, text, fnt, cx, y, color, int(255*min(1.,p*4)))

def punch_in(img, text, fnt_path, base_sz, cx, y, p, color):
    # Scale from 1.5x down to 1.0x with overshoot
    if p <= 0: return
    if p < 0.4:
        scale = 1.5 - 0.6*(p/0.4)   # 1.5 → 1.1 rapidly
    elif p < 0.6:
        scale = 1.0 + 0.15*math.sin((p-0.4)/0.2*math.pi)  # slight overshoot to 1.15
    else:
        scale = 1.0
    sz = max(8, int(base_sz*scale))
    f2 = fnt(fnt_path, sz)
    tw_alpha(img, text, f2, cx, y, color, int(255*min(1.,p*3)))

def bounce_in(img, text, fnt_path, base_sz, cx, y, p, color):
    scale = (1.3*(1-p/0.5)) if p<0.5 else (1.+0.08*(1-(p-.5)/.5))
    sz = max(8, int(base_sz*(1+scale*0.3)))
    f2 = fnt(fnt_path, sz)
    tw_alpha(img, text, f2, cx, y, color, int(255*min(1.,p*3)))

def grow_line(img, cx, y, maxw, p, color, h=3):
    if p<=0: return
    w = int(maxw*min(1.,p))
    if w<1: return
    o = Image.new("RGBA", img.size, (0,0,0,0))
    ImageDraw.Draw(o).rectangle([cx-w//2, y, cx+w//2, y+h], fill=color[:3]+(255,))
    img.alpha_composite(o)

def typewriter(img, text, fnt, cx, y, p, col_white, col_red, split_at):
    chars = max(0, int(p*len(text)))
    if not chars: return
    d0 = ImageDraw.Draw(Image.new("RGBA",(1,1)))
    fw = d0.textbbox((0,0), text, font=fnt)[2]
    x0 = cx - fw//2
    o = Image.new("RGBA", img.size, (0,0,0,0))
    d = ImageDraw.Draw(o)
    part1 = text[:min(chars, split_at)]
    part2 = text[split_at:chars] if chars > split_at else ""
    w1 = d.textbbox((0,0), text[:split_at], font=fnt)[2] if split_at > 0 else 0
    sk = {"stroke_width": 2, "stroke_fill": (0,0,0,200)}
    if part1: d.text((x0, y), part1, font=fnt, fill=col_white, **sk)
    if part2: d.text((x0+w1, y), part2, font=fnt, fill=col_red, **sk)
    img.alpha_composite(o)

def draw_subtitle(img, text, t, seg):
    # Strip em-dashes and en-dashes that look bad in karaoke chunks
    text = text.replace(" — ", " ").replace("—", "").replace(" – ", " ").strip()
    if not text: return
    seg_f0 = int(seg["start"]*FPS)
    seg_f1 = int(seg["end"]*FPS)
    cur_f  = int(t*FPS)
    elapsed   = cur_f - seg_f0
    remaining = seg_f1 - cur_f
    if elapsed < 3:     a = int(255 * elapsed / 3.0)
    elif remaining < 2: a = int(255 * remaining / 2.0)
    else: a = 255
    if a <= 0 or not text.strip(): return

    d0 = ImageDraw.Draw(Image.new("RGBA",(1,1)))
    bb = d0.textbbox((0,0), text, font=F_SUB)
    lw = bb[2]-bb[0]; lh = bb[3]-bb[1]

    # Clamp text width — never exceed 940px (50px margin each side)
    MAX_W = 940
    if lw > MAX_W:
        scale = MAX_W / lw
        lw = MAX_W
        lh = int(lh * scale)

    y   = 1660
    px, py = 28, 14
    x0 = max(20, CX - lw//2 - px)          # clamp left edge
    x1 = min(W - 20, CX + lw//2 + px)      # clamp right edge

    o_bg = Image.new("RGBA", img.size, (0,0,0,0))
    ImageDraw.Draw(o_bg).rounded_rectangle(
        [x0, y-py, x1, y+lh+py],
        radius=18, fill=(0,0,0,int(210*a/255))
    )
    img.alpha_composite(o_bg)
    tw_alpha(img, text, F_SUB, CX, y, (255,255,255), a)

F_LOGO_SM = fnt(BOLD, 32)   # skalestack.com — firma top-left

def draw_logo(img, a):
    a_dim = min(a, 180)
    o = Image.new("RGBA", img.size, (0,0,0,0))
    ImageDraw.Draw(o).text((48, 120), "SkaleStack.com", font=F_LOGO_SM,
                           fill=(255,255,255,int(a_dim)))
    img.alpha_composite(o)
    grow_line(img, 90, 162, 80, 1.0, GREEN, 2)

def draw_progress(img, f):
    bw = int(f/(TOTAL-1)*W)
    if bw<1: return
    o = Image.new("RGBA", img.size, (0,0,0,0))
    ImageDraw.Draw(o).rectangle([0,H-77,bw,H-73], fill=(0,255,136,255))
    img.alpha_composite(o)

# ── Overlay flash (white or red) ──────────────────────────────────────────────
def flash_overlay(img, color_rgba, alpha_0_255):
    if alpha_0_255 <= 0: return
    o = Image.new("RGBA", img.size, color_rgba[:3]+(int(alpha_0_255),))
    img.alpha_composite(o)

# ── Scene text — HIGH-TICKET v4 (jerarquía visual clara) ─────────────────────
# REGLA: máximo 3 elementos por escena. H1 domina, H2 contrasta, H3 es mínimo.
# COLORES: Blanco=statement autoridad, Verde=beneficio/CTA, Rojo=dolor/problema
def scene_text(img, sid, f, shake_dx=0, shake_dy=0):
    # REGLA: solo H1 + H2 por escena. H1 domina en tamaño y color. H2 contrasta.
    # sc1: f0=0   sc2: f0=127  sc3: f0=334  sc4: f0=489  sc5: f0=724  sc6: f0=901
    if sid == 1:
        p1=prog(f,3,6);  typewriter(img,"EL PROBLEMA",F_T88,CX,820,p1,(255,255,255,255),(255,255,255,255),0)
        p2=prog(f,14,8); punch_in(img,"No es el presupuesto.",REG,60,CX,970,p2,(255,59,59))

    elif sid == 2:
        p1=prog(f,130,6); punch_in(img,"MÁS TRÁFICO.",BOLD,88,CX,820,p1,(255,255,255))
        p2=prog(f,143,8); punch_in(img,"No convierte.",BOLD,56,CX,970,p2,(255,59,59))

    elif sid == 3:
        p1=prog(f,337,5); punch_in(img,"EXPERIMENTOS.",BOLD,88,CX,820,p1,(0,255,136))
        p2=prog(f,355,6); punch_in(img,"Datos. Velocidad.",BOLD,56,CX,970,p2,(255,255,255))

    elif sid == 4:
        p1=prog(f,492,8); punch_in(img,"SkaleStack.com",BOLD,96,CX,820,p1,(255,255,255))
        p2=prog(f,510,6); punch_in(img,"Experimenta. Mide. Escala.",BOLD,52,CX,970,p2,(0,255,136))

    elif sid == 5:
        p1=prog(f,727,6); punch_in(img,"EXCLUSIVO.",BOLD,96,CX,820,p1,(0,255,136))
        p2=prog(f,742,8); punch_in(img,"Solo startups B2B.",BOLD,56,CX,970,p2,(255,255,255))

    elif sid == 6:
        p1=prog(f,904,5); punch_in(img,"¿CALIFICAS?",BOLD,96,CX,820,p1,(0,255,136))
        p2=prog(f,920,6); punch_in(img,"SkaleStack.com",BOLD,72,CX,980,p2,(255,255,255))

# ── Transition functions ───────────────────────────────────────────────────────
def tr_fade_in(fr, p):
    return cv2.addWeighted(np.zeros_like(fr), 1-eoc(p), fr, eoc(p), 0)

def tr_whip_right(fa, fb, p):
    blur_k = max(1, int(p * 120)) | 1  # odd kernel
    if p < 0.45:
        # Outgoing: motion blur right + darken
        blurred = cv2.GaussianBlur(fa, (blur_k, 1), 0)
        return cv2.addWeighted(blurred, 1-p*1.5, np.zeros_like(fa), p*1.5, 0)
    else:
        # Incoming: unblur from left
        q = (p - 0.45) / 0.55
        blur_k2 = max(1, int((1-q)*80)) | 1
        blurred = cv2.GaussianBlur(fb, (blur_k2, 1), 0) if blur_k2 > 1 else fb
        return cv2.addWeighted(np.zeros_like(fb), 1-eoc(q), blurred, eoc(q), 0)

def tr_flash_white(fa, fb, p):
    if p < 0.4:
        q = p/0.4
        white = np.full_like(fa, 255)
        return cv2.addWeighted(fa, 1-q, white, q, 0)
    else:
        q = (p-0.4)/0.6
        white = np.full_like(fb, 255)
        return cv2.addWeighted(white, 1-eoc(q), fb, eoc(q), 0)

def tr_zoom_punch(fa, fb, p):
    # Rapid zoom into fa, then cut to fb
    if p < 0.5:
        q = p/0.5
        scale = 1.0 + 0.12*eio(q)
        ha,wa = fa.shape[:2]
        M = cv2.getRotationMatrix2D((wa/2,ha/2),0,scale)
        z = cv2.warpAffine(fa,M,(wa,ha))
        return cv2.addWeighted(z, 1-q*0.6, np.zeros_like(z), q*0.6, 0)
    else:
        q = (p-0.5)/0.5
        return cv2.addWeighted(np.zeros_like(fb), 1-eoc(q), fb, eoc(q), 0)

def tr_wipe_up(fa, fb, p):
    q = eoc(p)
    h_line = int(H * q)
    result = fa.copy()
    if h_line > 0:
        result[H-h_line:, :] = fb[H-h_line:, :]
    return result

def tr_fade_black(fr, p):
    a = 1.-eoc(p)
    return cv2.addWeighted(fr, a, np.zeros_like(fr), 1-a, 0)

# ── Main render ───────────────────────────────────────────────────────────────
def render():
    print(f"Renderizando {TOTAL} frames — v-ads-1 (emoción + transiciones)")
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f","rawvideo", "-vcodec","rawvideo",
        "-s",f"{W}x{H}", "-pix_fmt","rgb24", "-r",str(FPS),
        "-i","pipe:0",
        "-c:v","libx264", "-preset","fast", "-crf","22",
        "-pix_fmt","yuv420p",
        VIDEO_RAW
    ]
    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

    for cid in range(1,6):
        _caps[cid]=cv2.VideoCapture(CLIPS[cid])
        _fcounts[cid]=int(_caps[cid].get(cv2.CAP_PROP_FRAME_COUNT))

    for f in range(TOTAL):
        t = f/FPS
        sc = scene_at(f)
        sid = sc["id"]

        raw = crop916(get_bg(sc["clip"],f,sc))

        # Ken Burns — slow zoom per scene (skip for scene 6: black bg)
        if sc["clip"] != 0:
            raw = ken_burns(raw, f, sc)

        # ── Transitions ───────────────────────────────────────────────────────
        if f <= 5:
            raw = tr_fade_in(raw, f/5.)
        elif 106 <= f <= 126:
            nb = crop916(get_bg(2, SCENES[1]["f0"], SCENES[1]))
            nb = ken_burns(nb, SCENES[1]["f0"], SCENES[1])
            raw = tr_whip_right(raw, nb, (f-106)/20.)
        elif 313 <= f <= 333:
            nb = crop916(get_bg(3, SCENES[2]["f0"], SCENES[2]))
            nb = ken_burns(nb, SCENES[2]["f0"], SCENES[2])
            raw = tr_flash_white(raw, nb, (f-313)/20.)
        elif 468 <= f <= 488:
            nb = crop916(get_bg(4, SCENES[3]["f0"], SCENES[3]))
            nb = ken_burns(nb, SCENES[3]["f0"], SCENES[3])
            raw = tr_zoom_punch(raw, nb, (f-468)/20.)
        elif 703 <= f <= 723:
            nb = crop916(get_bg(5, SCENES[4]["f0"], SCENES[4]))
            nb = ken_burns(nb, SCENES[4]["f0"], SCENES[4])
            raw = tr_wipe_up(raw, nb, (f-703)/20.)
        elif 880 <= f <= 900:
            raw = tr_fade_black(raw, (f-880)/20.)
        elif 1183 <= f <= 1207:
            raw = tr_fade_black(raw, (f-1183)/24.)

        # Color tint per scene (applied BEFORE darken so tint doesn't get crushed)
        if sc["clip"] != 0:
            raw = apply_tint(raw, sid)

        raw = darken(raw, sc["alpha"])

        # Screen shake on hook reveal (frames 3-18)
        dx, dy = shake_offset(f, 3, duration=18, magnitude=9)
        if dx or dy:
            raw = apply_shake(raw, dx, dy)

        img = Image.fromarray(cv2.cvtColor(raw,cv2.COLOR_BGR2RGB)).convert("RGBA")

        # Impact flash overlay on hook text reveal (frames 3-8)
        if 3 <= f <= 10:
            flash_a = int(180 * max(0, 1 - (f-3)/7.))
            flash_overlay(img, (255,40,40), flash_a)

        draw_logo(img, int(230*min(1.,f/12.)))
        scene_text(img, sid, f)

        seg = srt_at(t)
        if seg: draw_subtitle(img, seg["text"], t, seg)

        draw_progress(img, f)

        proc.stdin.write(img.convert("RGB").tobytes())

        if f%50==0 or f==TOTAL-1:
            pct=(f+1)/TOTAL*100
            bar="█"*int(pct/5)+"░"*(20-int(pct/5))
            print(f"  [{bar}] {pct:5.1f}%  f={f} sc={sid}", end="\r", flush=True)

    proc.stdin.close(); proc.wait()
    for c in _caps.values(): c.release()
    print(f"\n  Video raw: {VIDEO_RAW}")

def assemble():
    print("Ensamblando audio (normalize=0, music 0.55)...")
    cmd = ["ffmpeg","-y","-i",VIDEO_RAW,"-i",AUDIO_OUT,
           "-c:v","copy","-c:a","aac","-b:a","128k","-shortest",VIDEO_OUT]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode!=0: print(r.stderr[-500:]); sys.exit(1)
    print(f"  Final: {VIDEO_OUT}")

def qa():
    print("\nQA —")
    r=subprocess.run(["ffprobe","-v","quiet","-show_entries",
                       "format=duration,size","-show_entries",
                       "stream=codec_name,width,height,r_frame_rate",
                       "-of","default",VIDEO_OUT],capture_output=True,text=True)
    print(r.stdout)
    r2=subprocess.run(["ffmpeg","-i",VIDEO_OUT,"-af","volumedetect","-f","null","/dev/null"],
                      capture_output=True,text=True)
    for l in r2.stderr.splitlines():
        if "volume" in l: print(" ",l.strip())

def preview_scenes():
    """Genera PNGs estáticos por escena en previews/ para validar texto antes de render."""
    import numpy as np, cv2
    prev_dir = f"{BASE}/previews"
    os.makedirs(prev_dir, exist_ok=True)
    samples = [(1,60,"sc1_hook"),(2,220,"sc2_problema"),(3,400,"sc3_solucion"),
               (4,600,"sc4_marca"),(5,800,"sc5_exclusivo"),(6,1050,"sc6_cta")]
    for sid, f, name in samples:
        bg = np.zeros((H,W,3), np.uint8); bg[:] = BLACK_BG
        img = Image.fromarray(cv2.cvtColor(bg,cv2.COLOR_BGR2RGB)).convert("RGBA")
        scene_text(img, sid, f)
        draw_logo(img, 230)
        img.convert("RGB").save(f"{prev_dir}/{name}.png")
        print(f"  {name}.png → {prev_dir}/")

if __name__=="__main__":
    import sys
    if "--preview" in sys.argv:
        preview_scenes()
        sys.exit(0)
    print("="*60)
    print("  SkaleStack Ad v4 — Emoción + Transiciones")
    print("="*60)
    render()
    assemble()
    qa()
    print(f"\n{'='*60}\n  LISTO → {VIDEO_OUT}  (v-ads-1)\n{'='*60}")
