"""Regenerate the public one-page campaign summary from the current figures."""

from pathlib import Path
from tempfile import TemporaryDirectory

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "downloads" / "campaign-summary.pdf"
PAGE_W, PAGE_H = A4
NAVY = colors.HexColor("#0f3042")
GOLD = colors.HexColor("#b4940d")
CREAM = colors.HexColor("#f8f6f0")
INK = colors.HexColor("#193447")
MUTED = colors.HexColor("#50606a")
FONT_DIR = Path("C:/Windows/Fonts")
pdfmetrics.registerFont(TTFont("Arial", str(FONT_DIR / "arial.ttf")))
pdfmetrics.registerFont(TTFont("Arial-Bold", str(FONT_DIR / "arialbd.ttf")))
pdfmetrics.registerFontFamily("Arial", normal="Arial", bold="Arial-Bold")


def paragraph(c, text, x, top, width, size=9.5, leading=14, color=INK, bold=False):
    style = ParagraphStyle(
        "body", fontName="Arial-Bold" if bold else "Arial", fontSize=size,
        leading=leading, textColor=color, spaceBefore=0, spaceAfter=0,
    )
    p = Paragraph(text, style)
    _, height = p.wrap(width, PAGE_H)
    p.drawOn(c, x, top - height)
    return top - height


def label(c, text, x, y, color=GOLD):
    c.setFillColor(color)
    c.setFont("Arial-Bold", 7.7)
    c.drawString(x, y, text.upper())


def rule(c, x1, y, x2):
    c.setStrokeColor(colors.HexColor("#d9d7ce"))
    c.setLineWidth(0.55)
    c.line(x1, y, x2, y)


def main():
    c = canvas.Canvas(str(OUTPUT), pagesize=A4)
    c.setTitle("A Home For Our City | Campaign summary")
    c.setAuthor("Christ Church Liverpool")
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    # Header
    c.setFillColor(NAVY)
    c.rect(0, PAGE_H - 112, PAGE_W, 112, fill=1, stroke=0)
    c.drawImage(str(ROOT / "photos" / "Logo-WIthBorder-Core.png"), 25, PAGE_H - 85, width=58, height=58, mask="auto", preserveAspectRatio=True)
    label(c, "A home for our city · capital campaign", 99, PAGE_H - 28, GOLD)
    c.setFont("Arial-Bold", 23)
    c.setFillColor(colors.white)
    c.drawString(99, PAGE_H - 54, "Christ Church Liverpool")
    paragraph(c, "A £5.5m goal to make 145 Edge Lane a permanent home for worship, training and serving Liverpool and beyond.", 99, PAGE_H - 64, 465, 10.5, 14.5, colors.HexColor("#e7edf0"))

    paragraph(c, "Liverpool needs more spaces for people to hear the gospel and grow in faith. Since 2003, Christ Church Liverpool has grown to a family of 250, planted or helped revitalise six churches, and sent workers across the world, all without a building of its own. Edge Lane changes what is possible.", 27, PAGE_H - 126, PAGE_W - 54, 9.5, 14, INK)

    # Main columns
    left, right = 27, 309
    label(c, "Why it matters", left, 630)
    c.setFont("Arial-Bold", 13)
    c.setFillColor(INK)
    c.drawString(left, 611, "Infrastructure for multiplication")
    why = [
        ("A strategic site", "On a main route into the city, alongside the university, hospital and research district."),
        ("A church with room to grow", "A 400-seat worship hall will allow the whole church to meet on one site."),
        ("A seven-day gospel hub", "Space for courses, youth work, community meals, training and prayer."),
        ("A training and sending base", "A home for raising up gospel workers for the region and the nations."),
    ]
    top = 594
    for title, body in why:
        c.setFillColor(GOLD)
        c.setFont("Arial-Bold", 10)
        c.drawString(left, top - 1, "›")
        top = paragraph(c, title, left + 13, top, 250, 9.6, 12, INK, True)
        top = paragraph(c, body, left + 13, top - 3, 249, 8.8, 12.5, MUTED) - 13

    with Image.open(ROOT / "photos" / "hero.jpg") as source:
        target_ratio = 254 / 108
        crop_height = int(source.width / target_ratio)
        crop_top = (source.height - crop_height) // 2
        photo = source.crop((0, crop_top, source.width, crop_top + crop_height))
        with TemporaryDirectory() as temp_dir:
            photo_path = Path(temp_dir) / "summary-photo.jpg"
            photo.save(photo_path, quality=82, optimize=True)
            c.drawImage(str(photo_path), left, 286, width=254, height=108)
    c.setFillColor(MUTED)
    c.setFont("Arial", 6.7)
    c.drawString(left, 277, "Artist's impression of 145 Edge Lane · subject to change")

    c.setStrokeColor(colors.HexColor("#ddd9ce"))
    c.line(295, 278, 295, 641)
    label(c, "The numbers", right, 630)
    c.setFont("Arial-Bold", 13)
    c.setFillColor(INK)
    c.drawString(right, 611, "Four clear phases")
    phases = [
        ("1", "Purchase & essential works", "£1.4m", "£1m purchase + £0.4m initial works"),
        ("2", "Full refurbishment", "up to £1.6m", "£1.5m–£2m total, including initial works"),
        ("3", "New worship hall", "£2.0m", "Purpose-built 400-seat hall"),
        ("4", "Third-floor space", "£0.5m", "Additional space for long-term use"),
    ]
    row_top = 593
    for number, title, amount, detail in phases:
        rule(c, right, row_top + 2, PAGE_W - 27)
        label(c, "Phase " + number, right, row_top - 14)
        paragraph(c, title, right + 60, row_top - 3, 151, 8.7, 11, INK, True)
        paragraph(c, detail, right + 60, row_top - 16, 151, 7.5, 9.4, MUTED)
        c.setFont("Arial-Bold", 9.1)
        c.setFillColor(INK)
        c.drawRightString(PAGE_W - 27, row_top - 14, amount)
        row_top -= 50
    rule(c, right, row_top + 2, PAGE_W - 27)
    c.setFont("Arial-Bold", 10)
    c.setFillColor(INK)
    c.drawString(right, row_top - 16, "Fundraising goal")
    c.setFillColor(GOLD)
    c.drawRightString(PAGE_W - 27, row_top - 16, "£5.5m")
    paragraph(c, "The goal uses the upper end of the refurbishment estimate.", right, row_top - 24, 255, 7.6, 10, MUTED)

    # Progress panel
    c.setFillColor(NAVY)
    c.rect(0, 190, PAGE_W, 77, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.setFont("Arial-Bold", 15)
    c.drawString(27, 235, "£1.64m raised and pledged")
    c.setFillColor(colors.white)
    c.setFont("Arial-Bold", 10)
    c.drawRightString(PAGE_W - 27, 238, "£3.86m still needed")
    paragraph(c, "£1.1m was used to buy the building. Around £0.54m has been pledged; most of it has already been given.", 27, 228, PAGE_W - 54, 8.6, 11.5, colors.HexColor("#e7edf0"))
    c.setFillColor(colors.HexColor("#526775"))
    c.roundRect(27, 202, PAGE_W - 54, 7, 3.5, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.roundRect(27, 202, (PAGE_W - 54) * 1.64 / 5.5, 7, 3.5, fill=1, stroke=0)

    # Invitation and footer
    c.setFillColor(GOLD)
    c.rect(0, 24, PAGE_W, 166, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Arial-Bold", 21)
    c.drawCentredString(PAGE_W / 2, 153, "Partner with us")
    invitations = [
        ("Pray", "Pray for provision and fruit."),
        ("Share", "Tell your church and network."),
        ("Give", "One-off gifts or regular giving."),
    ]
    for i, (heading, detail) in enumerate(invitations):
        x = 27 + i * 188
        c.setFont("Arial-Bold", 11)
        c.drawCentredString(x + 82, 119, heading)
        paragraph(c, detail, x, 108, 164, 8.3, 11, colors.white)
    c.setFont("Arial-Bold", 14)
    c.drawCentredString(PAGE_W / 2, 59, "homeforourcity.org")
    c.linkURL("https://homeforourcity.org", (195, 48, 400, 77), relative=0)
    c.setFillColor(INK)
    c.setFont("Arial", 7)
    c.drawString(27, 11, "Home For Our City · Christ Church Liverpool")
    c.drawRightString(PAGE_W - 27, 11, "office@christchurchliverpool.org · Charity No. 1125990")
    c.showPage()
    c.save()


if __name__ == "__main__":
    main()
