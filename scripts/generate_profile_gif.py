from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


BASE_WIDTH = 160
BASE_HEIGHT = 100
SCALE = 4
FRAME_COUNT = 24
FRAME_DURATION_MS = 90

COLORS = {
    "background": "#F8FBFC",
    "cloud": "#DCEEF2",
    "cloud_shadow": "#A9D8E2",
    "navy": "#17324D",
    "blue": "#2F80ED",
    "cyan": "#55C6D8",
    "cyan_dark": "#2398B3",
    "foam": "#F7FFFF",
    "mint": "#63D4B2",
    "yellow": "#F6C453",
    "coral": "#FF7A59",
    "skin": "#F2B38B",
    "white": "#FFFFFF",
}


def wave_height(x: int, phase: float) -> int:
    primary = math.sin((x + phase * 14) / 12)
    detail = math.sin((x - phase * 8) / 5) * 0.35
    return int(65 + primary * 5 + detail * 2)


def draw_cloud(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    c = COLORS["cloud"]
    s = COLORS["cloud_shadow"]
    draw.rectangle((x + 2, y + 3, x + 15, y + 6), fill=s)
    draw.rectangle((x, y + 1, x + 13, y + 4), fill=c)
    draw.rectangle((x + 3, y - 1, x + 7, y + 4), fill=c)
    draw.rectangle((x + 8, y, x + 11, y + 4), fill=c)
    draw.point((x + 15, y + 4), fill=c)


def draw_data_spark(draw: ImageDraw.ImageDraw, x: int, y: int, color: str) -> None:
    draw.point((x, y - 2), fill=color)
    draw.point((x, y + 2), fill=color)
    draw.point((x - 2, y), fill=color)
    draw.point((x + 2, y), fill=color)
    draw.point((x, y), fill=COLORS["white"])


def draw_character(draw: ImageDraw.ImageDraw, phase: float) -> None:
    x = 82
    surface_y = wave_height(x, phase)
    bob = int(math.sin(phase * math.tau) * 1.2)
    board_y = surface_y - 4 + bob

    # Board, legs, and hoodie.
    draw.rectangle((x - 10, board_y, x + 15, board_y + 1), fill=COLORS["yellow"])
    draw.rectangle((x - 7, board_y + 2, x + 11, board_y + 2), fill=COLORS["coral"])
    draw.line((x - 1, board_y - 7, x + 4, board_y - 2), fill=COLORS["navy"], width=2)
    draw.line((x + 4, board_y - 2, x + 10, board_y - 1), fill=COLORS["navy"], width=2)
    draw.rectangle((x - 4, board_y - 16, x + 3, board_y - 8), fill=COLORS["mint"])
    draw.rectangle((x - 6, board_y - 14, x - 4, board_y - 8), fill=COLORS["mint"])
    draw.point((x - 7, board_y - 9), fill=COLORS["skin"])

    # Head and wind-swept hair.
    draw.rectangle((x - 4, board_y - 23, x + 2, board_y - 17), fill=COLORS["skin"])
    draw.rectangle((x - 5, board_y - 24, x + 2, board_y - 22), fill=COLORS["navy"])
    draw.rectangle((x - 6, board_y - 23, x - 4, board_y - 20), fill=COLORS["navy"])
    draw.point((x + 1, board_y - 20), fill=COLORS["navy"])
    draw.point((x - 7, board_y - 24), fill=COLORS["navy"])
    draw.point((x - 8, board_y - 25), fill=COLORS["blue"])

    # Laptop and animated screen cursor.
    draw.polygon(
        [(x + 2, board_y - 15), (x + 11, board_y - 18), (x + 12, board_y - 10), (x + 3, board_y - 8)],
        fill=COLORS["navy"],
    )
    draw.polygon(
        [(x + 4, board_y - 14), (x + 9, board_y - 16), (x + 10, board_y - 12), (x + 5, board_y - 10)],
        fill=COLORS["blue"],
    )
    cursor_x = x + 6 + int((phase * 3) % 3)
    draw.point((cursor_x, board_y - 12), fill=COLORS["white"])
    draw.line((x - 1, board_y - 13, x + 4, board_y - 11), fill=COLORS["skin"], width=1)

    # Foam kick behind the board.
    trail = int((phase * 8) % 5)
    draw.line((x - 12 - trail, board_y + 1, x - 18 - trail, board_y - 2), fill=COLORS["foam"], width=2)
    draw.point((x - 20 - trail, board_y - 4), fill=COLORS["foam"])


def render_frame(frame_index: int) -> Image.Image:
    phase = frame_index / FRAME_COUNT
    image = Image.new("RGB", (BASE_WIDTH, BASE_HEIGHT), COLORS["background"])
    draw = ImageDraw.Draw(image)

    cloud_shift = int(phase * 18)
    draw_cloud(draw, 12 + cloud_shift, 18)
    draw_cloud(draw, 118 - cloud_shift // 2, 29)

    # Small code motifs drift through the open sky.
    font = ImageFont.load_default()
    draw.text((24, 39 + int(math.sin(phase * math.tau) * 2)), "{ }", fill=COLORS["blue"], font=font)
    draw.text((126, 17 + int(math.cos(phase * math.tau) * 2)), "AI", fill=COLORS["coral"], font=font)
    draw_data_spark(draw, 50, 22 + int(math.sin(phase * math.tau) * 2), COLORS["yellow"])
    draw_data_spark(draw, 111, 43 + int(math.cos(phase * math.tau) * 2), COLORS["mint"])

    surface = [(x, wave_height(x, phase)) for x in range(BASE_WIDTH)]
    draw.polygon(surface + [(BASE_WIDTH - 1, BASE_HEIGHT - 1), (0, BASE_HEIGHT - 1)], fill=COLORS["cyan"])
    draw.line(surface, fill=COLORS["cyan_dark"], width=1)

    # White foam and moving data pixels create the looping current.
    for x in range(-8, BASE_WIDTH + 8, 9):
        px = (x + frame_index * 2) % (BASE_WIDTH + 12) - 6
        y = wave_height(px, phase)
        if (x // 9 + frame_index) % 3 != 0:
            draw.rectangle((px, y - 1, px + 3, y), fill=COLORS["foam"])

    for row in range(4):
        for col in range(18):
            px = (col * 11 + row * 4 - frame_index * (1 + row % 2)) % BASE_WIDTH
            py = 73 + row * 7 + ((col + frame_index) % 3)
            color = COLORS["foam"] if (col + row) % 3 else COLORS["cyan_dark"]
            draw.rectangle((px, py, px + (col % 2), py + 1), fill=color)

    draw_character(draw, phase)

    # A thin dark baseline keeps the animation crisp on both GitHub themes.
    draw.line((0, BASE_HEIGHT - 1, BASE_WIDTH - 1, BASE_HEIGHT - 1), fill=COLORS["navy"], width=1)
    return image.resize((BASE_WIDTH * SCALE, BASE_HEIGHT * SCALE), Image.Resampling.NEAREST)


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
    print(f"Generated {gif_path} with {len(frames)} frames")


if __name__ == "__main__":
    main()
