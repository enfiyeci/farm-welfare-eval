# -*- coding: utf-8 -*-
"""report_theme — proven reportlab design system for data-heavy report PDFs.

Usage:
    import report_theme as theme
    theme.register_fonts()          # embeds Avenir Next + Charter (falls back to core fonts)
    S = theme.stylesheet()          # dict of ParagraphStyles: title/meta/h1/h2/kicker/body/quote/...
    tbl.setStyle(theme.booktabs(n_rows, header=True))
    story.append(theme.ScoreBar(7.5, vmax=10))
    doc.build(story, onFirstPage=theme.footer("My Report"), onLaterPages=theme.footer("My Report"))

Palette contract: ONE accent + neutral inks + a muted semantic trio used ONLY on data.
"""
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Flowable, TableStyle

# ---------------------------------------------------------------- palette
ACCENT = colors.HexColor("#0E5A6D")   # single accent (deep teal)
INK    = colors.HexColor("#1F2430")   # body text
GRAY   = colors.HexColor("#6A7180")   # meta / captions
RULE   = colors.HexColor("#D8DCE3")   # hairlines
ZEBRA  = colors.HexColor("#F6F8FA")   # optional row tint (very light)
PAPER_TINT = colors.HexColor("#EEF4F5")  # quote/callout background (barely-there accent tint)
GOOD = colors.HexColor("#2E7D5B")     # semantic trio — muted, data-only
WARN = colors.HexColor("#B97A2A")
BAD  = colors.HexColor("#A6474F")

# ---------------------------------------------------------------- fonts
_FONTS = {  # logical name -> (path, subfontIndex)  [macOS system fonts]
    "Head-Demi":   ("/System/Library/Fonts/Avenir Next.ttc", 2),
    "Head-Medium": ("/System/Library/Fonts/Avenir Next.ttc", 5),
    "Head-Reg":    ("/System/Library/Fonts/Avenir Next.ttc", 7),
    "Body":        ("/System/Library/Fonts/Supplemental/Charter.ttc", 0),
    "Body-Italic": ("/System/Library/Fonts/Supplemental/Charter.ttc", 1),
    "Body-Bold":   ("/System/Library/Fonts/Supplemental/Charter.ttc", 3),
}
_FALLBACK = {"Head-Demi": "Helvetica-Bold", "Head-Medium": "Helvetica-Bold", "Head-Reg": "Helvetica",
             "Body": "Times-Roman", "Body-Italic": "Times-Italic", "Body-Bold": "Times-Bold"}
FONT: dict = {}


def register_fonts() -> dict:
    """Register the embedded faces; on any failure fall back to core fonts (never crash a build)."""
    for name, (path, idx) in _FONTS.items():
        try:
            pdfmetrics.registerFont(TTFont(name, path, subfontIndex=idx))
            FONT[name] = name
        except Exception:
            FONT[name] = _FALLBACK[name]
    return FONT


def score_color(v, vmax=10.0):
    if v is None:
        return GRAY
    frac = v / vmax
    return GOOD if frac >= 0.85 else (WARN if frac >= 0.5 else BAD)


# ---------------------------------------------------------------- stylesheet
def stylesheet() -> dict:
    if not FONT:
        register_fonts()
    S = {}
    S["title"] = ParagraphStyle("title", fontName=FONT["Head-Demi"], fontSize=24, leading=28,
                                textColor=INK, spaceAfter=6)
    S["meta"] = ParagraphStyle("meta", fontName=FONT["Head-Reg"], fontSize=8.5, leading=12,
                               textColor=GRAY, spaceAfter=2)
    S["h1"] = ParagraphStyle("h1", fontName=FONT["Head-Demi"], fontSize=17, leading=21,
                             textColor=ACCENT, spaceBefore=16, spaceAfter=8)
    S["h2"] = ParagraphStyle("h2", fontName=FONT["Head-Demi"], fontSize=12.5, leading=16,
                             textColor=INK, spaceBefore=10, spaceAfter=4)
    S["kicker"] = ParagraphStyle("kicker", fontName=FONT["Head-Medium"], fontSize=8, leading=10,
                                 textColor=ACCENT, spaceBefore=6, spaceAfter=3)
    S["body"] = ParagraphStyle("body", fontName=FONT["Body"], fontSize=10, leading=14.5,
                               textColor=INK, spaceAfter=6, alignment=TA_LEFT)
    S["small"] = ParagraphStyle("small", fontName=FONT["Head-Reg"], fontSize=8, leading=11,
                                textColor=GRAY, spaceAfter=4)
    S["quote"] = ParagraphStyle("quote", fontName=FONT["Body-Italic"], fontSize=9.5, leading=13.5,
                                textColor=colors.HexColor("#123B47"), backColor=PAPER_TINT,
                                borderPadding=(6, 8, 6, 8), leftIndent=6, spaceBefore=9, spaceAfter=10)
    S["cell"] = ParagraphStyle("cell", fontName=FONT["Body"], fontSize=8.6, leading=11.5, textColor=INK)
    S["cellb"] = ParagraphStyle("cellb", fontName=FONT["Head-Medium"], fontSize=8.6, leading=11.5, textColor=INK)
    S["cellc"] = ParagraphStyle("cellc", parent=S["cell"], alignment=1)
    S["num"] = ParagraphStyle("num", fontName=FONT["Head-Medium"], fontSize=9, leading=11.5,
                              textColor=INK, alignment=2)  # numbers right-aligned
    return S


# ---------------------------------------------------------------- tables (booktabs — no cages)
def booktabs(n_rows: int, header: bool = True, zebra: bool = False,
             pad_v: float = 5, pad_h: float = 7) -> TableStyle:
    """Horizontal rules only: heavier top/bottom + header rule; generous padding; no vertical lines."""
    cmds = [
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), pad_v),
        ("BOTTOMPADDING", (0, 0), (-1, -1), pad_v),
        ("LEFTPADDING", (0, 0), (-1, -1), pad_h),
        ("RIGHTPADDING", (0, 0), (-1, -1), pad_h),
        ("LINEABOVE", (0, 0), (-1, 0), 1.0, ACCENT),
        ("LINEBELOW", (0, -1), (-1, -1), 1.0, ACCENT),
    ]
    if header:
        cmds.append(("LINEBELOW", (0, 0), (-1, 0), 0.75, ACCENT))
        first_data = 1
    else:
        first_data = 0
    for r in range(first_data, n_rows - 1):
        cmds.append(("LINEBELOW", (0, r), (-1, r), 0.4, RULE))
    if zebra:
        for r in range(first_data, n_rows):
            if (r - first_data) % 2 == 1:
                cmds.append(("BACKGROUND", (0, r), (-1, r), ZEBRA))
    return TableStyle(cmds)


# ---------------------------------------------------------------- score bar flowable
class ScoreBar(Flowable):
    """Inline horizontal score bar: track + value-colored fill + numeric label."""

    def __init__(self, value, vmax=10.0, width=0.85 * inch, height=7, label=True):
        super().__init__()
        self.value, self.vmax, self.width, self.height, self.label = value, vmax, width, height, label
        self._lw = 0.34 * inch if label else 0
    def wrap(self, *a):
        return self.width + self._lw, max(self.height, 9)
    def draw(self):
        c = self.canv
        y = 1
        c.setFillColor(colors.HexColor("#E8EBEF"))
        c.roundRect(0, y, self.width, self.height, self.height / 2, stroke=0, fill=1)
        if self.value is not None and self.vmax > 0:
            frac = max(0.0, min(1.0, self.value / self.vmax))
            if frac > 0:
                c.setFillColor(score_color(self.value, self.vmax))
                c.roundRect(0, y, max(self.width * frac, self.height), self.height,
                            self.height / 2, stroke=0, fill=1)
        if self.label:
            c.setFillColor(INK)
            c.setFont(FONT.get("Head-Medium", "Helvetica-Bold"), 8)
            txt = "N/A" if self.value is None else f"{self.value:.1f}"
            c.drawRightString(self.width + self._lw, y, txt)


# ---------------------------------------------------------------- page furniture
def footer(doc_title: str):
    def _draw(canvas, doc):
        canvas.saveState()
        canvas.setFont(FONT.get("Head-Reg", "Helvetica"), 7.5)
        canvas.setFillColor(GRAY)
        canvas.drawString(doc.leftMargin, 0.55 * inch, doc_title)
        canvas.drawRightString(doc.pagesize[0] - doc.rightMargin, 0.55 * inch, f"p. {doc.page}")
        canvas.setStrokeColor(RULE)
        canvas.setLineWidth(0.4)
        canvas.line(doc.leftMargin, 0.72 * inch, doc.pagesize[0] - doc.rightMargin, 0.72 * inch)
        canvas.restoreState()
    return _draw
