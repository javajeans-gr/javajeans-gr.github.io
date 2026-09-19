from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
SOURCE = Path(
    "/var/folders/5v/t3lx1lsx4cg9xj9414cp293c0000gn/T/"
    "codex-clipboard-1ef2c196-8488-45ea-bdca-f524f819b7a9.png"
)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def save_badges() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    source = Image.open(SOURCE).convert("RGBA")

    google = source.crop((28, 24, 548, 178))
    apple = source.crop((28, 207, 548, 360))

    apple.save(ASSETS / "app-store-badge.png")

    muted = ImageOps.grayscale(google.convert("RGB")).convert("RGBA")
    muted = ImageEnhance.Contrast(muted).enhance(0.72)
    muted = ImageEnhance.Brightness(muted).enhance(0.82)

    overlay = Image.new("RGBA", muted.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    label = "- Coming"
    label_font = font(26, bold=True)
    bbox = draw.textbbox((0, 0), label, font=label_font)
    x = muted.width - (bbox[2] - bbox[0]) - 28
    y = muted.height - (bbox[3] - bbox[1]) - 18
    draw.rounded_rectangle((x - 14, y - 8, muted.width - 16, muted.height - 10), radius=12, fill=(255, 255, 255, 34))
    draw.text((x, y), label, fill=(255, 255, 255, 230), font=label_font)

    muted = Image.alpha_composite(muted, overlay)
    muted.save(ASSETS / "google-play-badge-coming.png")


if __name__ == "__main__":
    save_badges()
