"""
Generate og-image.png (1200x630) — the social-share card for satwip.com.

Used by the og:image / twitter:image meta tags on every page, so link
previews on LinkedIn, X, Facebook, Slack, iMessage, etc. show a branded
card instead of a scraped fallback.

Design mirrors the site hero: dark brand background, "SAT" green + "WIP"
white (Segoe UI Bold), site tagline below in muted gray. Content is
centered with generous margins so platform-specific crops stay safe.

Output: SATWIP_WEBSITE/og-image.png
Run:    py tools/make_og_image.py
"""
import pathlib
from PIL import Image, ImageDraw, ImageFont

# Brand colours (mirror styles.css :root)
BG      = "#0d1117"
GREEN   = "#2ea043"
WHITE   = "#e6edf3"
MUTED   = "#8b949e"

W, H    = 1200, 630
MAX_WORD_W = 700                 # generous side margins for crop safety

FONT_BOLD     = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_SEMIBOLD = r"C:\Windows\Fonts\seguisb.ttf"   # falls back to bold if absent

TAGLINE = "Fundamental US stock screener"

HERE = pathlib.Path(__file__).resolve().parent
OUT  = HERE.parent / "og-image.png"


def _fit_font(path, text, max_w, start):
    size = start
    while size > 8:
        f = ImageFont.truetype(path, size)
        if f.getlength(text) <= max_w:
            return f
        size -= 2
    return ImageFont.truetype(path, 8)


def main():
    img = Image.new("RGB", (W, H), BG)
    d   = ImageDraw.Draw(img)

    word_font = _fit_font(FONT_BOLD, "SATWIP", MAX_WORD_W, start=220)
    sat_w  = word_font.getlength("SAT")
    full_w = word_font.getlength("SATWIP")
    wa, wd = word_font.getmetrics()
    word_h = wa + wd

    tag_path = FONT_SEMIBOLD if pathlib.Path(FONT_SEMIBOLD).exists() else FONT_BOLD
    tag_font = ImageFont.truetype(tag_path, max(28, round(word_font.size * 0.24)))
    tag_w = tag_font.getlength(TAGLINE)
    ta, td = tag_font.getmetrics()
    tag_h = ta + td

    gap = round(word_font.size * 0.28)

    block_h = word_h + gap + tag_h
    top = (H - block_h) // 2

    word_x = (W - full_w) / 2
    d.text((word_x, top), "SAT", font=word_font, fill=GREEN)
    d.text((word_x + sat_w, top), "WIP", font=word_font, fill=WHITE)

    d.text(((W - tag_w) / 2, top + word_h + gap), TAGLINE, font=tag_font, fill=MUTED)

    img.save(OUT, "PNG")
    print(f"Wrote {OUT}  ({W}x{H})")


if __name__ == "__main__":
    main()
