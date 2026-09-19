from pathlib import Path
import shutil
import subprocess
import textwrap

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
OUT = ASSETS / "clean-video"
LOGO = ASSETS / "aurora-logo.png"
VIDEO = ASSETS / "aurora-voiceover-demo.mp4"
POSTER = ASSETS / "aurora-voiceover-poster.jpg"
AUDIO = OUT / "aurora-voiceover.aiff"

W, H = 1920, 1080
INK = "#0b1328"
MUTED = "#64748b"
TEAL = "#0b8078"
AQUA = "#d9fbf5"
BLUE = "#2f80ed"
ORANGE = "#ff6b12"
RED = "#ef4444"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    names = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/SFNS.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica.ttc",
    ]
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()


F_TITLE = font(76, True)
F_H1 = font(94, True)
F_H2 = font(58, True)
F_BODY = font(36)
F_SMALL = font(28, True)


def canvas() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", (W, H), "#ffffff")
    draw = ImageDraw.Draw(img)
    for i in range(0, W, 3):
        tint = int(248 - 15 * (i / W))
        draw.line((i, 0, i, H), fill=(tint, 255, 252))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((-260, -180, 680, 720), fill=(217, 251, 245, 160))
    gd.ellipse((1300, -220, 2200, 520), fill=(238, 246, 255, 180))
    glow = glow.filter(ImageFilter.GaussianBlur(80))
    img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")
    return img, ImageDraw.Draw(img)


def rounded(draw: ImageDraw.ImageDraw, box, fill, outline="#dde8e7", radius=28, width=2):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def text(draw: ImageDraw.ImageDraw, xy, value, fnt, fill=INK, anchor=None, width=None, spacing=12):
    if width:
        lines = []
        for para in value.split("\n"):
            lines.extend(textwrap.wrap(para, width=width) or [""])
        draw.multiline_text(xy, "\n".join(lines), font=fnt, fill=fill, spacing=spacing, anchor=anchor)
    else:
        draw.text(xy, value, font=fnt, fill=fill, anchor=anchor)


def logo(draw: ImageDraw.ImageDraw, img: Image.Image, x=110, y=82, size=128):
    mark = Image.open(LOGO).convert("RGBA").resize((size, size), Image.Resampling.LANCZOS)
    shadow = Image.new("RGBA", (size + 44, size + 44), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((22, 22, size + 22, size + 22), radius=26, fill=(11, 19, 40, 42))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    img.paste(shadow, (x - 22, y - 22), shadow)
    img.paste(mark, (x, y), mark)
    text(draw, (x + size + 30, y + 28), "Aurora", F_H2, TEAL)
    text(draw, (x + size + 32, y + 92), "by Ragaven", F_BODY, MUTED)


def pill(draw, x, y, w, h, label, color=TEAL, fill="#ffffff"):
    rounded(draw, (x, y, x + w, y + h), fill, outline="#b6efe6", radius=24, width=2)
    text(draw, (x + w / 2, y + h / 2), label, F_SMALL, color, anchor="mm")


def slide_1(path):
    img, draw = canvas()
    logo(draw, img)
    text(draw, (150, 410), "Care intelligence\nfor aging adults.", F_H1, INK)
    text(draw, (154, 655), "Observe warning signs early. Keep care connected to action.", F_H2, TEAL)
    text(draw, (156, 770), "A calmer way for families and caregivers to know what is changing.", F_BODY, MUTED, width=60)
    img.save(path)


def slide_2(path):
    img, draw = canvas()
    text(draw, (160, 110), "Daily signals are scattered.", F_TITLE, INK)
    items = [("Vitals", "BP / HR / O2", TEAL), ("Labs", "Labs / Lipids", ORANGE), ("Meds", "Regularity", RED),
             ("Weight", "Trend", "#9b4de3"), ("Symptoms", "Notes", TEAL), ("Visits", "Schedule", BLUE)]
    for i, (head, sub, color) in enumerate(items):
        x = 180 + (i % 3) * 520
        y = 290 + (i // 3) * 245
        rounded(draw, (x, y, x + 420, y + 160), "#ffffff", outline="#dde8e7", radius=28)
        draw.ellipse((x + 34, y + 46, x + 98, y + 110), fill=color)
        text(draw, (x + 130, y + 48), head.upper(), F_SMALL, MUTED)
        text(draw, (x + 130, y + 92), sub, F_BODY, INK)
    text(draw, (160, 850), "Aurora brings the pieces together so families can act before a concern becomes urgent.", F_BODY, TEAL, width=72)
    img.save(path)


def slide_3(path):
    img, draw = canvas()
    text(draw, (160, 110), "From signals to care action.", F_TITLE, INK)
    left = (145, 330, 540, 650)
    mid = (760, 280, 1160, 700)
    right = (1380, 330, 1775, 650)
    rounded(draw, left, "#ffffff", outline="#b6efe6", radius=34)
    rounded(draw, mid, TEAL, outline=TEAL, radius=34)
    rounded(draw, right, "#ffffff", outline="#bfdbfe", radius=34)
    text(draw, (342, 420), "Daily\nsignals", F_H2, INK, anchor="mm")
    text(draw, (960, 410), "Aurora\nIntelligence\nEngine", F_H2, "#ffffff", anchor="mm")
    text(draw, (1578, 420), "Care alerts\ncommunicated", F_H2, INK, anchor="mm")
    text(draw, (650, 492), "→", font(92, True), TEAL, anchor="mm")
    text(draw, (1270, 492), "→", font(92, True), ORANGE, anchor="mm")
    pill(draw, 420, 735, 1080, 82, "Risk severity and proactive next steps", TEAL, "#edfffb")
    img.save(path)


def slide_4(path):
    img, draw = canvas()
    text(draw, (160, 110), "Two personas. One circle of care.", F_TITLE, INK)
    text(draw, (160, 215), "The Star is observed. Angels observe and care when help is needed.", F_BODY, MUTED)
    star = (210, 390, 840, 735)
    angels = (1080, 390, 1710, 735)
    rounded(draw, star, "#eff6ff", outline="#bfdbfe", radius=34, width=3)
    rounded(draw, angels, "#edfffb", outline="#a8f2e6", radius=34, width=3)
    text(draw, (525, 500), "Star", F_H2, BLUE, anchor="mm")
    text(draw, (525, 585), "Mom, dad, or\nsenior adult", F_BODY, MUTED, anchor="mm")
    text(draw, (1395, 500), "Angels", F_H2, TEAL, anchor="mm")
    text(draw, (1395, 585), "Family and\nprofessional caregivers", F_BODY, MUTED, anchor="mm")
    text(draw, (960, 558), "↔", font(100, True), TEAL, anchor="mm")
    pill(draw, 510, 810, 900, 90, "Observe updates. Get alerts. Help care move forward.", TEAL, "#edfffb")
    img.save(path)


def slide_5(path):
    img, draw = canvas()
    text(draw, (160, 110), "Proactive care + reactive alerts.", F_TITLE, INK)
    rounded(draw, (170, 300, 900, 770), "#edfffb", outline="#a8f2e6", radius=34)
    rounded(draw, (1020, 300, 1750, 770), "#eff6ff", outline="#bfdbfe", radius=34)
    text(draw, (230, 385), "Proactive care", F_H2, TEAL)
    text(draw, (1080, 385), "Reactive alerts", F_H2, BLUE)
    left = ["Medication missed", "Weight trending up", "BP above baseline", "Doctor follow-up due"]
    right = ["Abnormal vitals & risks", "Fall detected", "Aurora Help voice trigger", "Safe zone breach"]
    for i, label in enumerate(left):
        pill(draw, 240 + (i % 2) * 310, 500 + (i // 2) * 112, 260, 72, label, INK)
    for i, label in enumerate(right):
        pill(draw, 1090 + (i % 2) * 310, 500 + (i // 2) * 112, 260, 72, label, INK, "#ffffff")
    img.save(path)


def slide_6(path):
    img, draw = canvas()
    logo(draw, img, x=760, y=120, size=160)
    text(draw, (960, 440), "Less guessing.", F_H1, TEAL, anchor="mm")
    text(draw, (960, 555), "Earlier care conversations.", F_H2, INK, anchor="mm")
    text(draw, (960, 660), "More confidence between visits.", F_H2, INK, anchor="mm")
    pill(draw, 610, 805, 700, 90, "Built for families, caregivers, and care settings", TEAL, "#edfffb")
    img.save(path)


def build_video() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    slides = [slide_1, slide_2, slide_3, slide_4, slide_5, slide_6]
    durations = [6, 7, 7, 6, 7, 6]
    frame_paths = []
    for i, fn in enumerate(slides, 1):
        path = OUT / f"frame-{i:02d}.jpg"
        fn(path)
        frame_paths.append(path)

    POSTER.write_bytes(frame_paths[0].read_bytes())
    concat = OUT / "concat.txt"
    with concat.open("w") as fh:
        for frame, duration in zip(frame_paths, durations):
            fh.write(f"file '{frame}'\n")
            fh.write(f"duration {duration}\n")
        fh.write(f"file '{frame_paths[-1]}'\n")

    ffmpeg = shutil.which("ffmpeg") or "/opt/homebrew/bin/ffmpeg"
    silent = OUT / "silent.mp4"
    subprocess.run(
        [ffmpeg, "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-vf", "fps=30,format=yuv420p", str(silent)],
        check=True,
    )
    if AUDIO.exists():
        subprocess.run(
            [ffmpeg, "-y", "-i", str(silent), "-i", str(AUDIO), "-c:v", "copy", "-c:a", "aac", "-shortest", str(VIDEO)],
            check=True,
        )
    else:
        shutil.copyfile(silent, VIDEO)


if __name__ == "__main__":
    build_video()
