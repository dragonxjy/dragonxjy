from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


BASE_WIDTH = 240
BASE_HEIGHT = 140
SCALE = 3
FRAME_COUNT = 48
FRAME_DURATION_MS = 100

COLORS = {
    "wall": "#F5F8FA",
    "floor": "#DCE9EC",
    "floor_line": "#B6D1D7",
    "navy": "#18344F",
    "navy_dark": "#0E253A",
    "navy_light": "#2B506E",
    "blue": "#4385E8",
    "blue_light": "#91BDF5",
    "mint": "#59CDB1",
    "mint_dark": "#238A70",
    "yellow": "#F5C451",
    "coral": "#F4775B",
    "red": "#D94F55",
    "skin": "#F1B58E",
    "skin_shadow": "#D88E69",
    "wood": "#D6A45A",
    "wood_light": "#EDC778",
    "wood_dark": "#9C6534",
    "coffee": "#70452F",
    "white": "#FFFFFF",
    "screen": "#0D263A",
    "screen_dim": "#163A53",
}


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    filename = "consolab.ttf" if bold else "consola.ttf"
    try:
        return ImageFont.truetype(str(Path(r"C:\Windows\Fonts") / filename), size)
    except OSError:
        return ImageFont.truetype("DejaVuSansMono.ttf", size)


def animation_stage(frame: int) -> str:
    if frame < 12:
        return "typing"
    if frame < 22:
        return "success"
    if frame < 32:
        return "spill"
    if frame < 42:
        return "error"
    return "recovery"


def draw_spark(draw: ImageDraw.ImageDraw, x: int, y: int, color: str, size: int = 2) -> None:
    draw.line((x - size, y, x + size, y), fill=color)
    draw.line((x, y - size, x, y + size), fill=color)
    draw.point((x, y), fill=COLORS["white"])


def draw_background(draw: ImageDraw.ImageDraw, frame: int) -> None:
    draw.rectangle((0, 0, BASE_WIDTH - 1, 104), fill=COLORS["wall"])
    draw.rectangle((0, 105, BASE_WIDTH - 1, BASE_HEIGHT - 1), fill=COLORS["floor"])
    draw.line((0, 104, BASE_WIDTH - 1, 104), fill=COLORS["floor_line"], width=2)

    # Window with moving clouds and a small city skyline.
    draw.rectangle((16, 15, 79, 67), fill=COLORS["navy_light"])
    draw.rectangle((19, 18, 76, 64), fill="#D9EEFA")
    cloud_x = 27 + (frame // 3) % 34
    draw.rectangle((cloud_x, 27, cloud_x + 13, 30), fill=COLORS["white"])
    draw.rectangle((cloud_x + 4, 24, cloud_x + 9, 30), fill=COLORS["white"])
    draw.rectangle((24, 50, 34, 64), fill="#8FB6C6")
    draw.rectangle((36, 44, 47, 64), fill="#779FB2")
    draw.rectangle((49, 53, 57, 64), fill="#91B4C2")
    draw.rectangle((59, 39, 72, 64), fill="#6E97AB")
    draw.line((47, 18, 47, 64), fill=COLORS["navy_light"], width=2)
    draw.line((19, 42, 76, 42), fill=COLORS["navy_light"], width=2)

    # Shelf, books, and small plant add depth without crowding the scene.
    draw.rectangle((184, 22, 224, 25), fill=COLORS["wood_dark"])
    draw.rectangle((188, 12, 193, 22), fill=COLORS["coral"])
    draw.rectangle((194, 9, 199, 22), fill=COLORS["yellow"])
    draw.rectangle((200, 14, 205, 22), fill=COLORS["blue"])
    draw.rectangle((214, 16, 221, 22), fill=COLORS["wood"])
    draw.line((217, 16, 211, 10), fill=COLORS["mint_dark"], width=2)
    draw.line((218, 16, 224, 10), fill=COLORS["mint_dark"], width=2)
    draw.line((217, 16, 218, 7), fill=COLORS["mint"], width=2)

    font_small = load_font(7, bold=True)
    draw.rectangle((190, 43, 224, 64), fill="#FFF0B8", outline=COLORS["wood_dark"])
    draw.text((194, 47), "NO BUGS", fill=COLORS["navy"], font=font_small)
    draw.text((198, 55), "TODAY", fill=COLORS["coral"], font=font_small)

    # Rug and furniture shadows.
    draw.ellipse((36, 120, 222, 134), fill="#C4DDE1")
    draw.rectangle((48, 93, 55, 126), fill=COLORS["wood_dark"])
    draw.rectangle((211, 93, 218, 126), fill=COLORS["wood_dark"])
    draw.rectangle((179, 96, 207, 119), fill="#C28A48")
    draw.rectangle((183, 100, 203, 104), fill=COLORS["wood_light"])
    draw.rectangle((183, 108, 203, 112), fill=COLORS["wood_light"])

    # Chair and cable live behind the desk.
    draw.rectangle((53, 73, 67, 108), fill=COLORS["navy_dark"])
    draw.rectangle((58, 104, 88, 111), fill=COLORS["navy"])
    draw.line((66, 110, 62, 126), fill=COLORS["navy"], width=3)
    draw.line((82, 110, 87, 126), fill=COLORS["navy"], width=3)
    draw.line((62, 126, 56, 126), fill=COLORS["navy"], width=2)
    draw.line((87, 126, 93, 126), fill=COLORS["navy"], width=2)
    draw.arc((147, 84, 213, 118), 5, 145, fill=COLORS["navy_light"], width=1)

    draw.rectangle((43, 88, 221, 94), fill=COLORS["wood"])
    draw.rectangle((43, 88, 221, 90), fill=COLORS["wood_light"])
    draw.rectangle((43, 94, 221, 97), fill=COLORS["wood_dark"])


def draw_monitor(draw: ImageDraw.ImageDraw, frame: int, stage: str) -> None:
    shake = 0
    if stage == "error":
        shake = 1 if frame % 2 else -1
    x, y = 126 + shake, 31

    glow = {
        "typing": "#E3EEFB",
        "success": "#DDF3EC",
        "spill": "#E6F4EF",
        "error": "#F8DFE0",
        "recovery": "#E5EBF0",
    }[stage]
    draw.rectangle((x - 7, y - 7, x + 68, y + 58), fill=glow)
    draw.rectangle((x - 3, y - 3, x + 64, y + 54), fill="#D8E3E8")
    draw.rectangle((x, y, x + 61, y + 47), fill=COLORS["navy"])
    draw.rectangle((x + 5, y + 5, x + 56, y + 39), fill=COLORS["screen"])
    draw.rectangle((x + 28, y + 48, x + 34, y + 55), fill=COLORS["navy"])
    draw.rectangle((x + 18, y + 55, x + 44, y + 58), fill=COLORS["navy"])
    draw.rectangle((x + 7, y + 42, x + 9, y + 44), fill=COLORS["mint"])

    font_small = load_font(7)
    font_medium = load_font(9, bold=True)

    if stage == "typing":
        draw.text((x + 8, y + 7), "~/build", fill=COLORS["blue_light"], font=font_small)
        lengths = (29, 37, 23, 33)
        for row, length in enumerate(lengths):
            typed = max(5, min(length, frame * 5 - row * 4 + 7))
            color = COLORS["mint"] if row % 2 == 0 else COLORS["blue"]
            draw.rectangle((x + 9, y + 17 + row * 5, x + 9 + typed, y + 18 + row * 5), fill=color)
        cursor_x = x + 12 + (frame * 4) % 34
        draw.rectangle((cursor_x, y + 35, cursor_x + 2, y + 37), fill=COLORS["white"])
    elif stage in ("success", "spill"):
        draw.rectangle((x + 5, y + 5, x + 56, y + 39), fill=COLORS["mint_dark"])
        draw.text((x + 15, y + 10), "BUILD", fill=COLORS["white"], font=font_medium)
        draw.text((x + 10, y + 23), "PASSED!", fill="#D8FFF3", font=font_medium)
        draw.rectangle((x + 9, y + 35, x + 51, y + 36), fill=COLORS["mint"])
    elif stage == "error":
        draw.rectangle((x + 5, y + 5, x + 56, y + 39), fill=COLORS["red"])
        draw.text((x + 21, y + 9), "500", fill=COLORS["white"], font=font_medium)
        draw.text((x + 10, y + 24), "COFFEE.EXE", fill="#FFE5E5", font=font_small)
        draw.rectangle((x + 9, y + 35, x + 51, y + 36), fill="#FF9B9B")
    else:
        dots = "." * (1 + (frame - 42) % 3)
        draw.text((x + 10, y + 13), "rebooting" + dots, fill=COLORS["blue_light"], font=font_small)
        progress = min(38, (frame - 42) * 8)
        draw.rectangle((x + 9, y + 29, x + 49, y + 32), outline=COLORS["navy_light"])
        draw.rectangle((x + 10, y + 30, x + 10 + progress, y + 31), fill=COLORS["mint"])


def draw_keyboard(draw: ImageDraw.ImageDraw, frame: int, stage: str) -> None:
    draw.polygon([(121, 82), (169, 82), (177, 91), (114, 91)], fill=COLORS["navy_dark"])
    draw.line((119, 88, 172, 88), fill=COLORS["navy_light"], width=1)
    for row_y in (85, 88):
        offset = 0 if row_y == 85 else 2
        for x in range(124 + offset, 168, 6):
            draw.rectangle((x, row_y, x + 2, row_y + 1), fill=COLORS["floor_line"])

    if stage in ("spill", "error", "recovery"):
        spill_progress = 9 if stage != "spill" else max(0, frame - 22)
        spread = min(35, spill_progress * 4)
        draw.polygon(
            [(111, 89), (121 + spread, 87), (128 + spread, 92), (104, 94)],
            fill=COLORS["coffee"],
        )
        draw.point((126 + spread // 2, 96), fill=COLORS["coffee"])

    if stage == "error" and frame < 37:
        draw_spark(draw, 137, 80 - frame % 2, COLORS["yellow"], 3)
        draw_spark(draw, 154, 77 + frame % 2, COLORS["coral"], 2)


def draw_mug(draw: ImageDraw.ImageDraw, frame: int, stage: str) -> None:
    if stage in ("typing", "success"):
        draw.rectangle((104, 76, 114, 88), fill=COLORS["white"], outline=COLORS["navy"], width=1)
        draw.rectangle((114, 79, 119, 85), outline=COLORS["navy"], width=2)
        draw.rectangle((106, 76, 112, 78), fill=COLORS["coffee"])
        steam = frame % 6
        draw.arc((105, 67 - steam // 3, 110, 76), 100, 260, fill=COLORS["floor_line"], width=1)
        draw.arc((110, 65 + steam // 2, 115, 76), 100, 260, fill=COLORS["floor_line"], width=1)
    elif stage == "spill":
        progress = frame - 22
        x = 106 + progress * 2
        y = 79 + progress
        angle = min(8, progress)
        draw.polygon(
            [(x, y), (x + 10, y + angle // 2), (x + 8, y + 12), (x - 2, y + 8)],
            fill=COLORS["white"],
            outline=COLORS["navy"],
        )
        arc_end_x = 117 + progress * 4
        draw.line((x + 8, y + 5, arc_end_x, 88), fill=COLORS["coffee"], width=2)
        draw.point((arc_end_x + 2, 90), fill=COLORS["coffee"])
    else:
        draw.rectangle((125, 91, 137, 94), fill=COLORS["white"], outline=COLORS["navy"])
        draw.rectangle((136, 91, 141, 94), outline=COLORS["navy"])


def draw_character(draw: ImageDraw.ImageDraw, frame: int, stage: str) -> None:
    jitter = (1 if frame % 2 else -1) if stage == "error" else 0
    blink = stage == "typing" and frame in (5, 6)
    head_x, head_y = 78 + jitter, 47

    # Legs and shoes.
    draw.polygon([(75, 91), (84, 91), (79, 113), (72, 113)], fill="#315773")
    draw.polygon([(87, 91), (97, 91), (104, 112), (96, 114)], fill=COLORS["navy"])
    draw.rectangle((68, 112, 80, 116), fill=COLORS["navy_dark"])
    draw.rectangle((97, 111, 111, 115), fill=COLORS["navy_dark"])

    # Hoodie with shading and drawstrings.
    draw.polygon([(70, 68), (91, 65), (101, 74), (98, 93), (68, 93)], fill=COLORS["mint"])
    draw.polygon([(68, 79), (75, 75), (77, 92), (68, 93)], fill="#42B99C")
    draw.line((86, 68, 85, 78), fill=COLORS["white"], width=1)
    draw.line((91, 68, 92, 78), fill=COLORS["white"], width=1)
    draw.point((85, 79), fill=COLORS["navy"])
    draw.point((92, 79), fill=COLORS["navy"])

    # Head, ear, hair, and face.
    draw.rectangle((head_x, head_y, head_x + 16, head_y + 19), fill=COLORS["skin"])
    draw.rectangle((head_x - 2, head_y + 7, head_x + 1, head_y + 13), fill=COLORS["skin_shadow"])
    draw.polygon(
        [(head_x - 2, head_y + 1), (head_x + 4, head_y - 4), (head_x + 18, head_y - 2), (head_x + 18, head_y + 6), (head_x + 11, head_y + 4), (head_x + 6, head_y + 7), (head_x - 2, head_y + 7)],
        fill=COLORS["navy_dark"],
    )
    draw.rectangle((head_x + 5, head_y - 3, head_x + 13, head_y - 1), fill=COLORS["navy_light"])

    if stage == "error":
        draw.rectangle((head_x + 7, head_y + 10, head_x + 9, head_y + 12), fill=COLORS["white"])
        draw.rectangle((head_x + 13, head_y + 10, head_x + 15, head_y + 12), fill=COLORS["white"])
        draw.rectangle((head_x + 9, head_y + 16, head_x + 13, head_y + 17), fill=COLORS["navy"])
        draw_spark(draw, head_x + 20, head_y + 5, COLORS["blue"], 1)
    elif stage == "recovery":
        draw.line((head_x + 7, head_y + 11, head_x + 9, head_y + 11), fill=COLORS["navy"])
        draw.line((head_x + 13, head_y + 11, head_x + 15, head_y + 11), fill=COLORS["navy"])
        draw.line((head_x + 10, head_y + 16, head_x + 13, head_y + 15), fill=COLORS["navy"])
    else:
        eye_color = COLORS["skin"] if blink else COLORS["navy"]
        draw.rectangle((head_x + 13, head_y + 10, head_x + 14, head_y + 11), fill=eye_color)
        mouth_y = head_y + 15
        draw.line((head_x + 11, mouth_y, head_x + 15, mouth_y), fill=COLORS["navy"])

    if stage == "typing":
        hand_shift = frame % 2
        draw.line((96, 74, 112, 84 + hand_shift), fill=COLORS["mint"], width=5)
        draw.line((81, 76, 105, 86 - hand_shift), fill="#42B99C", width=5)
        draw.rectangle((108, 83 + hand_shift, 113, 87 + hand_shift), fill=COLORS["skin"])
        draw.rectangle((103, 84 - hand_shift, 108, 88 - hand_shift), fill=COLORS["skin"])
    elif stage == "success":
        bounce = frame % 2
        draw.line((74, 73, 61, 56 - bounce), fill="#42B99C", width=5)
        draw.line((98, 73, 111, 53 - bounce), fill=COLORS["mint"], width=5)
        draw.rectangle((58, 52 - bounce, 63, 57 - bounce), fill=COLORS["skin"])
        draw.rectangle((109, 49 - bounce, 114, 54 - bounce), fill=COLORS["skin"])
    elif stage == "spill":
        reach = min(12, frame - 22)
        draw.line((97, 74, 108 + reach, 78 + reach // 3), fill=COLORS["mint"], width=5)
        draw.rectangle((106 + reach, 77 + reach // 3, 112 + reach, 82 + reach // 3), fill=COLORS["skin"])
        draw.line((80, 76, 106, 86), fill="#42B99C", width=5)
    elif stage == "error":
        draw.line((72, 74, 57, 86 + frame % 2), fill="#42B99C", width=5)
        draw.line((99, 74, 115, 85 - frame % 2), fill=COLORS["mint"], width=5)
        draw.rectangle((53, 84 + frame % 2, 59, 89 + frame % 2), fill=COLORS["skin"])
        draw.rectangle((114, 82 - frame % 2, 120, 87 - frame % 2), fill=COLORS["skin"])
    else:
        draw.line((97, 72, 93, 56), fill=COLORS["mint"], width=5)
        draw.rectangle((87, 55, 95, 64), fill=COLORS["skin"])
        draw.line((79, 77, 108, 86), fill="#42B99C", width=5)


def draw_confetti(draw: ImageDraw.ImageDraw, frame: int, stage: str) -> None:
    if stage != "success":
        return
    fall = (frame - 12) * 3
    pieces = (
        (56, 25, "coral"),
        (91, 17, "yellow"),
        (116, 24, "blue"),
        (159, 13, "mint"),
        (199, 28, "coral"),
        (220, 14, "yellow"),
    )
    for index, (x, y, color) in enumerate(pieces):
        py = y + fall + index % 3
        draw.rectangle((x, py, x + 2, py + 4), fill=COLORS[color])


def render_frame(frame: int) -> Image.Image:
    stage = animation_stage(frame)
    image = Image.new("RGB", (BASE_WIDTH, BASE_HEIGHT), COLORS["wall"])
    draw = ImageDraw.Draw(image)

    draw_background(draw, frame)
    draw_monitor(draw, frame, stage)
    draw_keyboard(draw, frame, stage)
    draw_mug(draw, frame, stage)
    draw_character(draw, frame, stage)
    draw_confetti(draw, frame, stage)

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
    shared_palette = frames[0].quantize(colors=48, method=Image.Quantize.MEDIANCUT)
    indexed_frames = [
        frame.quantize(palette=shared_palette, dither=Image.Dither.NONE)
        for frame in frames
    ]
    gif_path = output_dir / "dragonxjy-coding.gif"
    indexed_frames[0].save(
        gif_path,
        save_all=True,
        append_images=indexed_frames[1:],
        duration=FRAME_DURATION_MS,
        loop=0,
        optimize=True,
        disposal=1,
    )
    generate_title(output_dir)
    print(f"Generated {gif_path} with {len(frames)} frames")


if __name__ == "__main__":
    main()
