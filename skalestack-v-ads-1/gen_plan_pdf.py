#!/usr/bin/env python3
"""Generate PLAN_V2.pdf — McKinsey style. Fixes: cover bleed, TOC numbers, emoji in code, ASCII table chars."""

import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (
    Paragraph, Spacer, Table, TableStyle, HRFlowable,
    Preformatted, PageBreak, NextPageTemplate,
    BaseDocTemplate, Frame, PageTemplate, Flowable
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

INPUT   = "/Users/jorgesaymar/Desktop/Video-editor-test/skalestack-v-ads-1/Plan de Producción Video ads v-ads-1.md"
OUTPUT  = "/Users/jorgesaymar/Desktop/Video-editor-test/skalestack-v-ads-1/Plan de Producción Video ads v-ads-1.pdf"
AD_NAME = "Las startups que ganan no gastan más — experimentan más rápido"
AD_SLUG = "skalestack-growth-hacking-ad"

PAGE_W, PAGE_H = A4

# ── Palette ───────────────────────────────────────────────────────────────────
BLACK      = colors.HexColor("#111111")
DARK_GRAY  = colors.HexColor("#333333")
MID_GRAY   = colors.HexColor("#555555")
LIGHT_GRAY = colors.HexColor("#888888")
RULE_GRAY  = colors.HexColor("#CCCCCC")
ALT_BG     = colors.HexColor("#F5F5F5")
CODE_BG    = colors.HexColor("#F0F0F0")
WHITE      = colors.white

# ── Styles ────────────────────────────────────────────────────────────────────
H1     = ParagraphStyle("H1",  fontSize=22, textColor=BLACK,     leading=28, fontName="Helvetica-Bold", spaceAfter=2*mm)
H2     = ParagraphStyle("H2",  fontSize=15, textColor=BLACK,     leading=20, fontName="Helvetica-Bold", spaceAfter=2*mm, spaceBefore=7*mm)
H3     = ParagraphStyle("H3",  fontSize=13, textColor=BLACK,     leading=17, fontName="Helvetica-Bold", spaceAfter=2*mm, spaceBefore=4*mm)
BODY   = ParagraphStyle("BD",  fontSize=10, textColor=DARK_GRAY, leading=15, fontName="Helvetica",      spaceAfter=2*mm)
BOLDB  = ParagraphStyle("BB",  fontSize=12, textColor=BLACK,     leading=17, fontName="Helvetica-Bold", spaceAfter=2*mm)
CODE_S = ParagraphStyle("CD",  fontSize=10, textColor=DARK_GRAY, backColor=CODE_BG, leading=14,
                         fontName="Courier", spaceAfter=3*mm,
                         leftIndent=3*mm, rightIndent=3*mm,
                         borderWidth=0.5, borderColor=RULE_GRAY, borderPad=4)
TOCTIT = ParagraphStyle("TT",  fontSize=16, textColor=BLACK,     leading=22, fontName="Helvetica-Bold", spaceAfter=5*mm)
TOCITM = ParagraphStyle("TI",  fontSize=12, textColor=DARK_GRAY, leading=18, fontName="Helvetica")
EXSUB  = ParagraphStyle("ES",  fontSize=12, textColor=BLACK,     leading=17, fontName="Helvetica-Bold", spaceAfter=2*mm, spaceBefore=5*mm)
QUOTE  = ParagraphStyle("QS",  fontSize=13, textColor=MID_GRAY,  leading=19, fontName="Helvetica-Oblique",
                         leftIndent=8*mm, rightIndent=8*mm, spaceAfter=3*mm, spaceBefore=3*mm)

# ── Page callbacks ────────────────────────────────────────────────────────────
def cover_page(canvas, doc):
    canvas.saveState()
    w, h = A4
    # Top bar
    canvas.setFillColor(BLACK)
    canvas.rect(0, h - 22*mm, w, 22*mm, fill=1, stroke=0)
    canvas.setFont("Helvetica-Bold", 9)
    canvas.setFillColor(WHITE)
    canvas.drawString(15*mm, h - 13*mm, "SkaleStack.com")
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(LIGHT_GRAY)
    canvas.drawRightString(w - 15*mm, h - 13*mm, "CONFIDENCIAL")
    # Titles
    canvas.setFont("Helvetica-Bold", 26)
    canvas.setFillColor(BLACK)
    canvas.drawString(15*mm, h - 68*mm, "PLAN DE PRODUCCION VIDEO ADS")
    canvas.setFont("Helvetica-Bold", 20)
    canvas.setFillColor(MID_GRAY)
    canvas.drawString(15*mm, h - 82*mm, "v-ads-1")
    canvas.setFont("Helvetica-Oblique", 10)
    canvas.setFillColor(MID_GRAY)
    canvas.drawString(15*mm, h - 91*mm, f'"{AD_NAME}"')
    # Thick rule
    canvas.setStrokeColor(BLACK)
    canvas.setLineWidth(2.5)
    canvas.line(15*mm, h - 97*mm, w - 15*mm, h - 97*mm)
    # Metadata
    meta = [
        ("Nombre del anuncio", AD_NAME[:50] + "…" if len(AD_NAME) > 50 else AD_NAME),
        ("Slug / ID",          AD_SLUG),
        ("Estado",             "Activo — documento unico"),
        ("Fecha",              "2026-05-13"),
        ("Render",             "RE-RENDER PENDIENTE — TTS guion nuevo"),
        ("Duracion estimada",  "~38 segundos"),
        ("Plataforma",         "Instagram Ads — Reels"),
        ("Formato",            "1080 x 1920 px | 9:16 | 30fps | H.264/AAC"),
        ("Preparado por",      "Claude Code / SkaleStack"),
    ]
    y = h - 109*mm
    for label, value in meta:
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(LIGHT_GRAY)
        canvas.drawString(15*mm, y, label.upper())
        canvas.setFont("Helvetica-Bold", 8.5)
        canvas.setFillColor(BLACK)
        canvas.drawString(58*mm, y, value)
        y -= 8*mm
    # Thin rule
    canvas.setStrokeColor(RULE_GRAY)
    canvas.setLineWidth(0.5)
    canvas.line(15*mm, y - 2*mm, w - 15*mm, y - 2*mm)
    # Status block — left column
    y2 = y - 14*mm
    canvas.setFont("Helvetica-Bold", 7)
    canvas.setFillColor(LIGHT_GRAY)
    canvas.drawString(15*mm, y2, "ESTADO DE PRODUCCION")
    y2 -= 6*mm
    phases = [
        ("Guion v4",        True),
        ("TTS — voz",       True),
        ("Stock footage",   True),
        ("Audio mix",       True),
        ("Render v7",       True),
        ("Re-render v8",    False),
        ("QA final",        False),
    ]
    for phase, done in phases:
        canvas.setFillColor(BLACK if done else RULE_GRAY)
        canvas.rect(15*mm, y2 - 1*mm, 2.5*mm, 2.5*mm, fill=1, stroke=0)
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(BLACK if done else LIGHT_GRAY)
        canvas.drawString(20*mm, y2, phase)
        y2 -= 6*mm
    # Bottom bar
    canvas.setFillColor(BLACK)
    canvas.rect(0, 0, w, 10*mm, fill=1, stroke=0)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(LIGHT_GRAY)
    canvas.drawCentredString(w / 2, 3.5*mm, "skalestack.com")
    canvas.restoreState()


def inner_page(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setStrokeColor(BLACK)
    canvas.setLineWidth(1.5)
    canvas.line(15*mm, h - 12*mm, w - 15*mm, h - 12*mm)
    canvas.setFont("Helvetica-Bold", 7)
    canvas.setFillColor(BLACK)
    canvas.drawString(15*mm, h - 10*mm, "PLAN DE PRODUCCION VIDEO ADS — v-ads-1")
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(LIGHT_GRAY)
    canvas.drawRightString(w - 15*mm, h - 10*mm, "CONFIDENCIAL | 2026-05-13")
    canvas.setStrokeColor(RULE_GRAY)
    canvas.setLineWidth(0.5)
    canvas.line(15*mm, 10*mm, w - 15*mm, 10*mm)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(LIGHT_GRAY)
    # Page 1 is cover, page 2 is exec summary = "1", page 3 = TOC, page 4+ = content
    canvas.drawCentredString(w / 2, 6.5*mm, str(doc.page - 1))
    canvas.restoreState()


# ── Text helpers ──────────────────────────────────────────────────────────────
# FIX: strip emoji from plain text (used in headings etc.)
def strip_emoji(text):
    text = re.sub(r"✅|✓", "", text)
    text = re.sub(r"⏳|❌|⚠️|🔊|📐|⏱️|📝|🎞️", "", text)
    return text.strip()

# FIX: clean code block text — replace box-drawing chars and emojis with ASCII equivalents
def clean_code(text):
    # Box-drawing / decorative chars that Helvetica/Courier can't render
    replacements = {
        "═": "=", "─": "-", "│": "|", "┌": "+", "┐": "+",
        "└": "+", "┘": "+", "├": "+", "┤": "+", "┬": "+", "┴": "+", "┼": "+",
        "→": "->", "←": "<-", "↓": "v", "↑": "^",
        "✅": "[OK]", "⏳": "[...]", "❌": "[X]", "⚠️": "[!]",
        "✔": "[OK]",  # ✔
    }
    for bad, good in replacements.items():
        text = text.replace(bad, good)
    return text

def pi(text):
    """Parse inline markdown for Paragraph (reportlab XML)."""
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\*(.+?)\*",    r"<i>\1</i>", text)
    text = re.sub(r"`(.+?)`",      r'<font name="Courier" size="7.5">\1</font>', text)
    # Strip all emoji cleanly
    text = re.sub(r"✅|✓|✔", "", text)
    text = re.sub(r"⏳", "[ ]", text)
    text = re.sub(r"❌", "[X]", text)
    text = re.sub(r"⚠️", "[!]", text)
    return text.strip()


def thin_rule(story):
    story.append(HRFlowable(width="100%", thickness=0.5, color=RULE_GRAY,
                            spaceBefore=1*mm, spaceAfter=2*mm))

def thick_rule(story):
    story.append(HRFlowable(width="100%", thickness=1.5, color=BLACK,
                            spaceBefore=0, spaceAfter=3*mm))

def sub_rule(story):
    story.append(HRFlowable(width="15%", thickness=1.5, color=BLACK,
                            spaceBefore=0, spaceAfter=2*mm))

def is_sep(raw):
    return bool(re.match(r"^\|[\s\-\|:]+\|?\s*$", raw))


def flush_table(table_block, story):
    rows = []
    for line in table_block:
        if is_sep(line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows.append(cells)
    if not rows:
        return
    col_count = max(len(r) for r in rows)
    rows = [r + [""] * (col_count - len(r)) for r in rows]

    hdr_s = ParagraphStyle("TH", fontSize=11, leading=15, fontName="Helvetica-Bold", textColor=WHITE)
    bdy_s = ParagraphStyle("TC", fontSize=10, leading=14, fontName="Helvetica",      textColor=DARK_GRAY)
    cod_s = ParagraphStyle("TK", fontSize=10, leading=14, fontName="Courier",        textColor=DARK_GRAY)

    para_rows = []
    for ri, row in enumerate(rows):
        if ri == 0:
            para_rows.append([Paragraph(pi(c), hdr_s) for c in row])
        else:
            styled = []
            for c in row:
                # Use courier for cells that look like file paths / code
                if "/" in c or c.startswith("`") or re.match(r"^\d+\.\d+s?$", c):
                    styled.append(Paragraph(pi(c), cod_s))
                else:
                    styled.append(Paragraph(pi(c), bdy_s))
            para_rows.append(styled)

    col_w = (180 * mm) / col_count
    t = Table(para_rows, colWidths=[col_w] * col_count, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  BLACK),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  WHITE),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, ALT_BG]),
        ("GRID",          (0, 0), (-1, -1), 0.5, RULE_GRAY),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",    (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING",   (0, 0), (-1, -1), 5),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 5),
    ]))
    story.append(t)
    story.append(Spacer(1, 3*mm))


# Extract title keeping the section number (for body headings)
def h2_body(raw_h2):
    """'## 3. LÍNEA DE TIEMPO' -> '3. LÍNEA DE TIEMPO' (keeps number)"""
    title = re.sub(r"^#{2,3}\s*", "", raw_h2).strip()
    return strip_emoji(title)

# Extract title without number (for TOC — number comes from the counter)
def toc_title_clean(raw_h2):
    """'## 3. LÍNEA DE TIEMPO' -> 'LÍNEA DE TIEMPO'"""
    title = re.sub(r"^#{2,3}\s*", "", raw_h2).strip()
    title = re.sub(r"^\d+[a-z]?\.\s*", "", title)
    return strip_emoji(title)


# Anchor flowable: records actual page number for a section during build
_section_pages = {}   # populated during first pass: {section_num -> page}

class SectionAnchor(Flowable):
    def __init__(self, section_num):
        super().__init__()
        self.section_num = section_num
        self.width = 0
        self.height = 0

    def draw(self):
        _section_pages[self.section_num] = self.canv._pageNumber


def build_toc(sections, page_map=None):
    """Build TOC with H2 and H3 levels. sections = [(level, key, title), ...]"""
    items = []
    items.append(Paragraph("Indice de Contenido", TOCTIT))
    thick_rule(items)

    h2_s  = ParagraphStyle("T2", fontSize=11, textColor=BLACK,     fontName="Helvetica-Bold", leading=15)
    h3_s  = ParagraphStyle("T3", fontSize=10, textColor=DARK_GRAY, fontName="Helvetica",      leading=14)
    pg2_s = ParagraphStyle("P2", fontSize=10, textColor=BLACK,     fontName="Helvetica-Bold", alignment=TA_RIGHT)
    pg3_s = ParagraphStyle("P3", fontSize=9,  textColor=LIGHT_GRAY,fontName="Helvetica",      alignment=TA_RIGHT)
    dot_s = ParagraphStyle("DT", fontSize=8,  textColor=LIGHT_GRAY,fontName="Helvetica",      alignment=TA_RIGHT)

    for level, key, title in sections:
        page_str = str(page_map.get(key, "")) if (page_map and key in page_map) else ("…" if level == 2 else "")

        if level == 2:
            if key is not None and str(key).isdigit():
                label = f"<b>{key}.</b>  {title}"
            else:
                label = f"<b>{title}</b>"
            indent   = 0
            txt_s    = h2_s
            pg_s     = pg2_s
            dots     = "." * 16
            top_pad  = 2
            bot_pad  = 2
            show_line = True
        else:  # H3
            label    = f"  {title}"
            indent   = 6*mm
            txt_s    = h3_s
            pg_s     = pg3_s
            dots     = "." * 12
            top_pad  = 0
            bot_pad  = 0
            show_line = False

        row = Table(
            [[Paragraph(label, txt_s),
              Paragraph(dots, dot_s),
              Paragraph(page_str, pg_s)]],
            colWidths=[140*mm - indent, 28*mm, 12*mm],
        )
        style = [
            ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING",    (0, 0), (-1, -1), top_pad),
            ("BOTTOMPADDING", (0, 0), (-1, -1), bot_pad),
            ("LEFTPADDING",   (0, 0), (-1, -1), 0),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
        ]
        if show_line:
            style.append(("LINEBELOW", (0, 0), (-1, 0), 0.5, RULE_GRAY))
        row.setStyle(TableStyle(style))

        if indent:
            row = Table([[Spacer(indent, 1), row]], colWidths=[indent, 180*mm - indent])
            row.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                                     ("LEFTPADDING",(0,0),(-1,-1),0),
                                     ("RIGHTPADDING",(0,0),(-1,-1),0),
                                     ("TOPPADDING",(0,0),(-1,-1),0),
                                     ("BOTTOMPADDING",(0,0),(-1,-1),0)]))

        items.append(row)
        items.append(Spacer(1, 0.5*mm if level == 2 else 0.2*mm))
    return items


def exec_summary():
    story = []
    story.append(Paragraph("Resumen Ejecutivo", H1))
    thick_rule(story)

    story.append(Paragraph("QUE ES ESTE VIDEO", EXSUB))
    sub_rule(story)
    story.append(Paragraph(
        "Un anuncio de 31 segundos para YouTube Shorts y Reels, formato 9:16 vertical. "
        "Disenado para interrumpir el scroll de fundadores y lideres de startups B2B "
        "que gastan en marketing sin ver resultados medibles. "
        "El video no vende un producto — vende un cambio de mentalidad: "
        "<b>de gastar en marketing a construir un sistema de crecimiento.</b>",
        BODY))

    story.append(Paragraph("ANGULO DE VENTA", EXSUB))
    sub_rule(story)
    story.append(Paragraph(
        "El angulo central es el <b>dolor del desperdicio</b>: la startup promedio gasta en ads, "
        "agencias y contenido sin construir traccion real. SkaleStack posiciona el "
        "<b>Growth Hacking con IA</b> como la alternativa inteligente — no mas gasto, "
        "mas velocidad de experimentacion.",
        BODY))
    story.append(Paragraph(
        '"La mayoria de startups muere gastando en marketing. Las que sobreviven hacen Growth Hacking."',
        QUOTE))
    story.append(Paragraph(
        "Este hook activa dos emociones simultaneas: <b>miedo</b> (mi startup podria morir) "
        "y <b>esperanza</b> (hay un camino diferente). El resto del video entrega la promesa "
        "en capas: identifica el problema › define el metodo › presenta la empresa › "
        "cierra con CTA de bajo compromiso.",
        BODY))

    story.append(Paragraph("PUBLICO OBJETIVO", EXSUB))
    sub_rule(story)
    tgt_data = [
        ("Perfil",            "Fundadores y CMOs de startups B2B — etapa seed a serie A"),
        ("Dolor principal",   "Gastan en marketing pero el numero no se mueve"),
        ("Creencia que rompe","Necesito mas presupuesto para crecer"),
        ("Creencia que instala","Necesito un sistema de experimentos, no mas gasto"),
        ("CTA esperado",      "Agendar sesion gratis en skalestack.com"),
    ]
    l_s = ParagraphStyle("LS", fontSize=10, leading=14, fontName="Helvetica-Bold", textColor=BLACK)
    v_s = ParagraphStyle("VS", fontSize=10, leading=14, fontName="Helvetica",      textColor=DARK_GRAY)
    tgt_rows = [[Paragraph(l, l_s), Paragraph(v, v_s)] for l, v in tgt_data]
    tgt_t = Table(tgt_rows, colWidths=[50*mm, 130*mm])
    tgt_t.setStyle(TableStyle([
        ("ROWBACKGROUNDS", (0,0),(-1,-1), [WHITE, ALT_BG]),
        ("GRID",           (0,0),(-1,-1), 0.5, RULE_GRAY),
        ("VALIGN",         (0,0),(-1,-1), "TOP"),
        ("TOPPADDING",     (0,0),(-1,-1), 4),
        ("BOTTOMPADDING",  (0,0),(-1,-1), 4),
        ("LEFTPADDING",    (0,0),(-1,-1), 5),
        ("RIGHTPADDING",   (0,0),(-1,-1), 5),
    ]))
    story.append(tgt_t)
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("ESTRUCTURA NARRATIVA", EXSUB))
    sub_rule(story)
    arc_data = [
        ["#", "Escena", "Rol narrativo", "Dur."],
        ["1", "Hook",       "Golpe de realidad — la mayoria muere gastando",          "5.1s"],
        ["2", "Problema",   "Amplifica el dolor — pagas trafico, no crecimiento",     "5.8s"],
        ["3", "Que es",     "Presenta el metodo — experimentos, datos, velocidad",    "4.7s"],
        ["4", "SkaleStack", "Empresa como solucion — Growth Hacking + IA",            "6.0s"],
        ["5", "Identidad",  "Diferenciador — vendemos metodo medible, no promesas",   "2.9s"],
        ["6", "CTA",        "Accion de bajo compromiso — sesion gratis",              "6.0s"],
    ]
    a_h = ParagraphStyle("AH", fontSize=11, leading=15, fontName="Helvetica-Bold", textColor=WHITE)
    a_b = ParagraphStyle("AB", fontSize=10, leading=14, fontName="Helvetica",      textColor=DARK_GRAY)
    arc_rows = []
    for ri, row in enumerate(arc_data):
        st = a_h if ri == 0 else a_b
        arc_rows.append([Paragraph(c, st) for c in row])
    arc_t = Table(arc_rows, colWidths=[10*mm, 28*mm, 112*mm, 30*mm], repeatRows=1)
    arc_t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,0),  BLACK),
        ("TEXTCOLOR",     (0,0),(-1,0),  WHITE),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, ALT_BG]),
        ("GRID",          (0,0),(-1,-1), 0.5, RULE_GRAY),
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
        ("TOPPADDING",    (0,0),(-1,-1), 3),
        ("BOTTOMPADDING", (0,0),(-1,-1), 3),
        ("LEFTPADDING",   (0,0),(-1,-1), 5),
        ("RIGHTPADDING",  (0,0),(-1,-1), 5),
    ]))
    story.append(arc_t)
    story.append(Spacer(1, 5*mm))

    # Project folder
    story.append(Paragraph("ESTRUCTURA DEL PROYECTO", EXSUB))
    sub_rule(story)
    story.append(Paragraph(
        "Base del proyecto: "
        "<font name='Courier' size='7.5'>/Users/jorgesaymar/Desktop/Video-editor-test/skalestack-v-ads-1/</font>",
        BODY))
    folder_data = [
        ["Archivo / Carpeta", "Descripcion", "Estado"],
        ["PLAN_V2.md / .pdf",            "Plan de produccion completo — este documento",          "Completo"],
        ["audio/voice_v2_dionisio.wav",  "Voz referencia XTTS-v2 Dionisio — no modificar",     "Listo"],
        ["audio/music_beyond.mp3",       "Musica cinematic dark — 205s (AShamaluevMusic)",      "Listo"],
        ["audio/music_strength.mp3",     "Alternativa A — 194s corporativo/power",              "Listo"],
        ["audio/music_foundation.mp3",   "Alternativa B — 196s contemplativo",                  "Listo"],
        ["stock/new_clip1_money_loss.mp4","Escena 1 — animacion perdida de dinero — 9:16",     "Listo"],
        ["stock/new_clip2_dark_laptop.mp4","Escena 2 — laptop cuarto oscuro — 9:16",           "Listo"],
        ["stock/new_clip3_analytics.mp4","Escena 3 — analytics / datos — 9:16",                "Listo"],
        ["stock/new_clip4_man_camera.mp4","Escena 4 — hombre barbado camara — 9:16",           "Listo"],
        ["stock/new_clip5_confident.mp4","Escena 5 — hombre traje camara — 9:16",              "Listo"],
        ["output/skalestack_v7.mp4",     "Ultimo render (guion v3, obsoleto)",                  "Obsoleto"],
        ["output/v-ads-1.mp4",           "Video final — destino del proximo render",            "Pendiente"],
        ["/tmp/skalestack_v3/*.srt",     "SRT guion v3 — reemplazar tras nuevo TTS",           "Temporal"],
    ]
    f_h  = ParagraphStyle("FH", fontSize=11, leading=15, fontName="Helvetica-Bold", textColor=WHITE)
    f_b  = ParagraphStyle("FB", fontSize=10, leading=14, fontName="Helvetica",      textColor=DARK_GRAY)
    f_c  = ParagraphStyle("FC", fontSize=10, leading=14, fontName="Courier",        textColor=DARK_GRAY)
    f_rows = []
    for ri, row in enumerate(folder_data):
        if ri == 0:
            f_rows.append([Paragraph(c, f_h) for c in row])
        else:
            f_rows.append([Paragraph(row[0], f_c), Paragraph(row[1], f_b), Paragraph(row[2], f_b)])
    f_t = Table(f_rows, colWidths=[62*mm, 92*mm, 26*mm], repeatRows=1)
    f_t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,0),  BLACK),
        ("TEXTCOLOR",     (0,0),(-1,0),  WHITE),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, ALT_BG]),
        ("GRID",          (0,0),(-1,-1), 0.5, RULE_GRAY),
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
        ("TOPPADDING",    (0,0),(-1,-1), 3),
        ("BOTTOMPADDING", (0,0),(-1,-1), 3),
        ("LEFTPADDING",   (0,0),(-1,-1), 5),
        ("RIGHTPADDING",  (0,0),(-1,-1), 5),
    ]))
    story.append(f_t)
    story.append(PageBreak())
    return story


# ── Markdown parser ───────────────────────────────────────────────────────────
def parse_md(path, page_map=None):
    with open(path, "r", encoding="utf-8") as f:
        lines = [l.rstrip("\n") for l in f]

    # Collect sections for TOC: (level, key, title)
    # level 2 = ##, level 3 = ###
    # key = section number (int) for numbered H2, None for unnumbered, "2.1" string for H3
    sections = []
    cur_h2_key = None
    h3_idx = 0
    for line in lines:
        raw = line.strip()
        if raw.startswith("### "):
            bare = strip_emoji(re.sub(r"^###\s*", "", raw).strip())
            h3_idx += 1
            key = f"{cur_h2_key}.{h3_idx}" if cur_h2_key is not None else f"0.{h3_idx}"
            sections.append((3, key, bare))
        elif raw.startswith("## "):
            bare = re.sub(r"^##\s*", "", raw).strip()
            bare = strip_emoji(bare)
            num_match = re.match(r"^(\d+)\.\s+(.*)", bare)
            if num_match:
                cur_h2_key = int(num_match.group(1))
                h3_idx = 0
                sections.append((2, cur_h2_key, num_match.group(2).strip()))
            else:
                cur_h2_key = None
                h3_idx = 0
                sections.append((2, None, bare))

    story = []

    # ── Cover
    story.append(Spacer(1, PAGE_H))
    story.append(NextPageTemplate("inner"))
    story.append(PageBreak())

    # ── TOC (page 2 — inmediatamente tras portada)
    story += build_toc(sections, page_map=page_map)
    story.append(PageBreak())

    # ── Executive summary (page 3)
    story += exec_summary()

    # ── Content
    i = 0
    in_code     = False
    code_lines  = []
    in_table    = False
    table_block = []
    skip_h1     = True          # H1 is on cover, skip it in content
    cur_h2_num  = None          # current H2 number (for H3 sub-numbering)
    h3_counter  = 0             # resets on each new H2

    while i < len(lines):
        line = lines[i]
        raw  = line.strip()

        # Code block
        if raw.startswith("```"):
            if in_table:
                flush_table(table_block, story); table_block = []; in_table = False
            if in_code:
                cleaned = clean_code("\n".join(code_lines))
                story.append(Preformatted(cleaned, CODE_S))
                story.append(Spacer(1, 2*mm))
                code_lines = []; in_code = False
            else:
                in_code = True
            i += 1; continue

        if in_code:
            code_lines.append(line)
            i += 1; continue

        # Table
        if raw.startswith("|"):
            if not in_table: in_table = True
            table_block.append(raw)
            i += 1; continue
        else:
            if in_table:
                flush_table(table_block, story); table_block = []; in_table = False

        # HR
        if raw == "---":
            thin_rule(story)
            i += 1; continue

        # H1 — skip (on cover)
        if re.match(r"^# [^#]", raw):
            if skip_h1:
                skip_h1 = False
                i += 1; continue
            story.append(Paragraph(pi(strip_emoji(raw[2:])), H1))
            thick_rule(story)
            i += 1; continue

        # Bold metadata line (e.g. **Fecha:** ...)
        if raw.startswith("**") and "|" not in raw:
            story.append(Paragraph(pi(raw), BOLDB))
            i += 1; continue

        # H2 — keeps section number to match TOC
        if raw.startswith("## "):
            sec_title = h2_body(raw)
            num_match = re.match(r"^(\d+)", sec_title)
            if num_match:
                cur_h2_num = int(num_match.group(1))
                story.append(SectionAnchor(cur_h2_num))
            else:
                cur_h2_num = None
            h3_counter = 0
            story.append(Paragraph(pi(sec_title), H2))
            story.append(HRFlowable(width="20%", thickness=1.5, color=BLACK,
                                    spaceBefore=0, spaceAfter=2*mm))
            i += 1; continue

        # H3 — auto-number as X.Y if inside a numbered H2
        if raw.startswith("### "):
            clean = strip_emoji(re.sub(r"^###\s*", "", raw))
            h3_counter += 1
            h3_key = f"{cur_h2_num}.{h3_counter}" if cur_h2_num is not None else f"0.{h3_counter}"
            story.append(SectionAnchor(h3_key))
            if cur_h2_num is not None:
                clean = f"{cur_h2_num}.{h3_counter}  {clean}"
            story.append(Paragraph(pi(clean), H3))
            i += 1; continue

        # Empty
        if raw == "":
            story.append(Spacer(1, 1*mm))
            i += 1; continue

        # Normal paragraph
        story.append(Paragraph(pi(raw), BODY))
        i += 1

    # Flush leftovers
    if in_code and code_lines:
        story.append(Preformatted(clean_code("\n".join(code_lines)), CODE_S))
    if in_table and table_block:
        flush_table(table_block, story)

    return story, sections


# ── Build ─────────────────────────────────────────────────────────────────────
def make_doc(output_path):
    doc = BaseDocTemplate(
        output_path, pagesize=A4,
        leftMargin=15*mm, rightMargin=15*mm,
        topMargin=18*mm, bottomMargin=16*mm,
        title="PLAN DE PRODUCCION VIDEO ADS — v-ads-1",
        author="SkaleStack",
    )
    cover_frame = Frame(0, 0, PAGE_W, PAGE_H,
                        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    inner_frame = Frame(15*mm, 16*mm, PAGE_W - 30*mm, PAGE_H - 34*mm,
                        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[cover_frame], onPage=cover_page),
        PageTemplate(id="inner", frames=[inner_frame], onPage=inner_page),
    ])
    return doc


def build_story(sections, page_map=None):
    """Build the full story. Pass page_map on second pass to get real page numbers."""
    story, _ = parse_md(INPUT)
    # Inject TOC with page numbers — find where TOC was inserted and replace it
    # TOC is inserted as part of parse_md; we need to rebuild with updated TOC.
    # Since parse_md builds the TOC inline, we rebuild from scratch here.
    return story


def main():
    import tempfile, os

    # ── Pass 1: build to temp file to collect section page numbers
    _section_pages.clear()
    story1, sections = parse_md(INPUT)
    tmp = tempfile.mktemp(suffix=".pdf")
    doc1 = make_doc(tmp)
    doc1.build(story1)
    page_map = dict(_section_pages)  # {section_num -> page}

    # ── Pass 2: rebuild with real page numbers in TOC
    _section_pages.clear()
    story2, sections2 = parse_md(INPUT, page_map=page_map)
    doc2 = make_doc(OUTPUT)
    doc2.build(story2)

    os.unlink(tmp)
    print(f"PDF generado: {OUTPUT}")
    print(f"  Numeros de pagina del indice: {page_map}")


if __name__ == "__main__":
    main()
