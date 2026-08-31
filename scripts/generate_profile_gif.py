from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


BASE_WIDTH = 180
BASE_HEIGHT = 105
SCALE = 4
FRAME_COUNT = 36
FRAME_DURATION_MS = 110

COLORS = {
    "background": "#F8FBFC",
    "floor": "#E5F1F3",
    "line": "#B6D5DB",
    "navy": "#17324D",
    "blue": "#2F80ED",
    "screen": "#102A43",
    "screen_line": "#63D4B2",
    "green": "#238A70",
    "red": "#D94F4F",
    "mint": "#63D4B2",
    "yellow": "#F6C453",
    "coral": "#FF7A59",
    "skin": "#F2B38B",
    "desk": "#DDAF63",
    "desk_dark": "#A86F35",
    "coffee": "#7C4A2D",
    "white": "#FFFFFF",
}


def draw_spark(draw: ImageDraw.ImageDraw, x: int, y: int, color: str) -> None:
    draw.point((x, y - 2), fill=color)
    draw.point((x, y + 2), fill=color)
    draw.point((x - 2, y), fill=color)
    draw.point((x + 2, y), fill=color)
    draw.point((x, y), fill=COLORS["white"])


def draw_room(draw: ImageDraw.ImageDraw) -> None:
    draw.rectangle((0, 0, BASE_WIDTH - 1, 77), fill=COLORS["background"])
    draw.rectangle((0, 78, BASE_WIDTH - 1, BASE_HEIGHT - 1), fill=COLORS["floor"])
    draw.line((0, 77, BASE_WIDTH - 1, 77), fill=COLORS["line"])

    font = ImageFont.load_default()
    draw.rectangle((19, 18, 47, 38), outline=COLORS["line"], width=1)
    draw.text((25, 24), "SHIP", fill=COLORS["blue"], font=font)
    draw.rectangle((137, 19, 160, 40), outline=COLORS["line"], width=1)
    draw.text((143, 25), "404", fill=COLORS["coral"], font=font)

    draw.ellipse((28, 90, 152, 98), fill="#D0E5E8")
    draw.rectangle((27, 63, 155, 67), fill=COLORS["desk"])
    draw.rectangle((31, 67, 36, 94), fill=COLORS["desk_dark"])
    draw.rectangle((147, 67, 152, 94), fill=COLORS["desk_dark"])


def draw_monitor(draw: ImageDraw.ImageDraw, frame: int) -> None:
    is_error = 23 <= frame <= 30
    shake = (1 if frame % 2 else -1) if is_error else 0
    x = 82 + shake
    y = 24

    draw.rectangle((x, y, x + 43, y + 34), fill=COLORS["navy"])
    draw.rectangle((x + 4, y + 4, x + 39, y + 28), fill=COLORS["screen"])
    draw.rectangle((x + 19, y + 35, x + 24, y + 39), fill=COLORS["navy"])
    draw.rectangle((x + 12, y + 39, x + 31, y + 41), fill=COLORS["navy"])

    font = ImageFont.load_default()
    if frame < 9:
        line_lengths = (18, 25, 13, 21)
        for row, length in enumerate(line_lengths):
            visible = max(3, min(length, frame * 4 - row * 2 + 5))
            color = COLORS["screen_line"] if row % 2 == 0 else COLORS["blue"]
            draw.rectangle((x + 7, y + 7 + row * 5, x + 7 + visible, y + 8 + row * 5), fill=color)
    elif frame < 23:
        draw.rectangle((x + 4, y + 4, x + 39, y + 28), fill=COLORS["green"])
        draw.text((x + 10, y + 8), "IT", fill=COLORS["white"], font=font)
        draw.text((x + 6, y + 16), "WORKS", fill=COLORS["white"], font=font)
    elif frame <= 30:
        draw.rectangle((x + 4, y + 4, x + 39, y + 28), fill=COLORS["red"])
        draw.text((x + 13, y + 12), "500", fill=COLORS["white"], font=font)
    else:
        dots = "." * (1 + (frame - 31) % 3)
        draw.text((x + 15, y + 12), dots, fill=COLORS["screen_line"], font=font)


def draw_keyboard(draw: ImageDraw.ImageDraw, frame: int) -> None:
    draw.polygon([(83, 59), (118, 59), (123, 64), (79, 64)], fill=COLORS["navy"])
    for x in range(84, 117, 5):
        draw.point((x, 61), fill=COLORS["line"])
    if 20 <= frame <= 29:
        spill = min(20, (frame - 19) * 3)
        draw.rectangle((79, 62, 79 + spill, 64), fill=COLORS["coffee"])
        draw.point((86 + spill // 2, 66), fill=COLORS["coffee"])
    if 23 <= frame <= 26:
        draw_spark(draw, 96, 58 - (frame % 2), COLORS["yellow"])
        draw_spark(draw, 106, 55 + (frame % 2), COLORS["coral"])


def draw_mug(draw: ImageDraw.ImageDraw, frame: int) -> None:
    if frame < 17:
        draw.rectangle((70, 55, 76, 62), fill=COLORS["white"], outline=COLORS["navy"])
        draw.rectangle((76, 57, 79, 60), outline=COLORS["navy"])
        draw.rectangle((71, 55, 75, 56), fill=COLORS["coffee"])
        if frame % 4 in (0, 1):
            draw.point((72, 52), fill=COLORS["line"])
            draw.point((75, 50), fill=COLORS["line"])
    elif frame < 23:
        progress = frame - 17
        x = 72 + progress
        y = 57 + progress // 2
        draw.polygon([(x, y), (x + 7, y + 3), (x + 5, y + 8), (x - 1, y + 5)], fill=COLORS["white"], outline=COLORS["navy"])
        draw.line((x + 6, y + 4, 82 + progress * 2, 63), fill=COLORS["coffee"], width=2)
    else:
        draw.rectangle((83, 64, 91, 66), fill=COLORS["white"], outline=COLORS["navy"])
        draw.rectangle((90, 64, 93, 66), outline=COLORS["navy"])


def draw_character(draw: ImageDraw.ImageDraw, frame: int) -> None:
    typing = frame < 9
    celebrating = 9 <= frame < 17
    spilling = 17 <= frame < 23
    error = 23 <= frame <= 30
    recovering = frame > 30
    jitter = (frame % 2) if error else 0

    # Chair and body.
    draw.rectangle((39, 54, 47, 78), fill=COLORS["navy"])
    draw.rectangle((42, 76, 61, 81), fill=COLORS["navy"])
    draw.line((45, 81, 43, 91), fill=COLORS["navy"], width=2)
    draw.line((58, 81, 61, 91), fill=COLORS["navy"], width=2)
    draw.rectangle((48 + jitter, 48, 62 + jitter, 66), fill=COLORS["mint"])

    # Head and hair.
    head_y = 35 - (1 if celebrating and frame % 2 else 0)
    draw.rectangle((50 + jitter, head_y, 60 + jitter, head_y + 12), fill=COLORS["skin"])
    draw.rectangle((49 + jitter, head_y - 2, 61 + jitter, head_y + 1), fill=COLORS["navy"])
    draw.rectangle((48 + jitter, head_y, 51 + jitter, head_y + 6), fill=COLORS["navy"])

    if error:
        draw.rectangle((53 + jitter, head_y + 5, 54 + jitter, head_y + 6), fill=COLORS["white"])
        draw.rectangle((58 + jitter, head_y + 5, 59 + jitter, head_y + 6), fill=COLORS["white"])
        draw.point((55 + jitter, head_y + 10), fill=COLORS["navy"])
        draw.point((62 + jitter, head_y + 2), fill=COLORS["blue"])
        draw.point((64 + jitter, head_y + 5), fill=COLORS["blue"])
    else:
        draw.point((59 + jitter, head_y + 5), fill=COLORS["navy"])
        draw.line((56 + jitter, head_y + 9, 59 + jitter, head_y + 9), fill=COLORS["navy"])

    if typing:
        hand_y = 59 + frame % 2
        draw.line((60, 53, 72, hand_y), fill=COLORS["mint"], width=3)
        draw.point((73, hand_y), fill=COLORS["skin"])
    elif celebrating:
        draw.line((50, 52, 42, 42), fill=COLORS["mint"], width=3)
        draw.line((61, 52, 70, 41), fill=COLORS["mint"], width=3)
        draw.point((41, 40), fill=COLORS["skin"])
        draw.point((71, 39), fill=COLORS["skin"])
    elif spilling:
        draw.line((60, 54, 72 + (frame - 17), 57), fill=COLORS["mint"], width=3)
        draw.point((73 + (frame - 17), 57), fill=COLORS["skin"])
    elif error:
        draw.line((49, 54, 40, 60 + frame % 2), fill=COLORS["mint"], width=3)
        draw.line((61, 54, 70, 60 - frame % 2), fill=COLORS["mint"], width=3)
        draw.point((39, 61 + frame % 2), fill=COLORS["skin"])
        draw.point((71, 61 - frame % 2), fill=COLORS["skin"])
    elif recovering:
        draw.line((60, 52, 57, 42), fill=COLORS["mint"], width=3)
        draw.rectangle((54, 40, 59, 45), fill=COLORS["skin"])


def draw_confetti(draw: ImageDraw.ImageDraw, frame: int) -> None:
    if not 9 <= frame < 17:
        return
    fall = (frame - 9) * 2
    pieces = ((72, 16, "coral"), (96, 10, "yellow"), (127, 16, "blue"), (143, 9, "mint"), (32, 12, "yellow"))
    for index, (x, y, color) in enumerate(pieces):
        py = y + fall + index % 3
        draw.rectangle((x, py, x + 1, py + 2), fill=COLORS[color])


def render_frame(frame: int) -> Image.Image:
    image = Image.new("RGB", (BASE_WIDTH, BASE_HEIGHT), COLORS["background"])
    draw = ImageDraw.Draw(image)
    draw_room(draw)
    draw_monitor(draw, frame)
    draw_keyboard(draw, frame)
    draw_mug(draw, frame)
    draw_character(draw, frame)
    draw_confetti(draw, frame)
    return image.resize((BASE_WIDTH * SCALE, BASE_HEIGHT * SCALE), Image.Resampling.NEAREST)


def generate_title(output_dir: Path) -> None:
    width, height = 1000, 150
    image = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype(r"C:\Windows\Fonts\Inkfree.ttf", 76)
    except OSError:
        font = ImageFont.truetype("DejaVuSans.ttf", 76)
    text = "Hey, I'm Dragon_xjy."
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    x = (width - text_width) // 2
    draw.text((x, 18), text, font=font, fill=COLORS["navy"])
    underline_y = 116
    draw.line(
        [(x + 50, underline_y), (x + text_width // 2, underline_y + 5), (x + text_width - 38, underline_y - 1)],
        fill=COLORS["coral"],
        width=5,
    )
    image.save(output_dir / "dragonxjy-title.png", optimize=True)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    output_dir = root / "assets"
    output_dir.mkdir(parents=True, exist_ok=True)

    frames = [render_frame(index) for index in range(FRAME_COUNT)]
    gif_path = output_dir / "dragonxjy-coding.gif"
    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=FRAME_DURATION_MS,
        loop=0,
        optimize=True,
        disposal=2,
    )
    generate_title(output_dir)
    print(f"Generated {gif_path} with {len(frames)} frames")


if __name__ == "__main__":
    main()
