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
    "wall_warm": "#FBF7E9",
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
    "skin_light": "#FFD0A8",
    "hoodie_light": "#79DDC4",
    "denim": "#315773",
    "denim_light": "#466E89",
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
    draw.polygon([(19, 61), (76, 61), (145, 104), (92, 104)], fill=COLORS["wall_warm"])
    draw.rectangle((0, 105, BASE_WIDTH - 1, BASE_HEIGHT - 1), fill=COLORS["floor"])
    draw.line((0, 104, BASE_WIDTH - 1, 104), fill=COLORS["floor_line"], width=2)
    draw.line((18, 122, 222, 122), fill="#D1E2E5")
    draw.line((52, 105, 38, 139), fill="#D1E2E5")
    draw.line((190, 105, 207, 139), fill="#D1E2E5")

    # A quiet wall clock and drifting dust make the room feel lived in.
    draw.ellipse((91, 15, 108, 32), fill="#D5E3E7", outline=COLORS["navy_light"], width=2)
    draw.ellipse((94, 18, 105, 29), fill=COLORS["white"])
    clock_tick = (frame // 4) % 8
    hand_x = 100 + int(round(math.sin(clock_tick * math.pi / 4) * 4))
    hand_y = 24 - int(round(math.cos(clock_tick * math.pi / 4) * 4))
    draw.line((100, 24, hand_x, hand_y), fill=COLORS["navy"], width=1)
    draw.line((100, 24, 97, 27), fill=COLORS["coral"], width=1)
    for index, (x, y) in enumerate(((72, 76), (85, 85), (101, 91), (117, 98))):
        drift = (frame // 3 + index * 2) % 7
        draw.point((x + drift, y - drift // 2), fill="#E8DFAF")

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
    for x, y in ((27, 54), (31, 58), (39, 50), (43, 55), (63, 45), (68, 50)):
        draw.rectangle((x, y, x + 1, y + 2), fill="#D9EEF5")
    draw.line((47, 18, 47, 64), fill=COLORS["navy_light"], width=2)
    draw.line((19, 42, 76, 42), fill=COLORS["navy_light"], width=2)
    draw.line((22, 20, 43, 40), fill="#EDF8FD")
    draw.line((50, 20, 72, 40), fill="#EDF8FD")

    # Shelf, books, and small plant add depth without crowding the scene.
    draw.rectangle((184, 22, 224, 25), fill=COLORS["wood_dark"])
    draw.rectangle((188, 12, 193, 22), fill=COLORS["coral"])
    draw.rectangle((194, 9, 199, 22), fill=COLORS["yellow"])
    draw.rectangle((200, 14, 205, 22), fill=COLORS["blue"])
    draw.rectangle((214, 16, 221, 22), fill=COLORS["wood"])
    draw.rectangle((215, 17, 219, 21), fill=COLORS["wood_light"])
    draw.line((217, 16, 211, 10), fill=COLORS["mint_dark"], width=2)
    draw.line((218, 16, 224, 10), fill=COLORS["mint_dark"], width=2)
    draw.line((217, 16, 218, 7), fill=COLORS["mint"], width=2)
    draw.point((211, 9), fill=COLORS["hoodie_light"])
    draw.point((224, 9), fill=COLORS["hoodie_light"])

    font_small = load_font(7, bold=True)
    draw.rectangle((192, 45, 226, 66), fill="#D9E4E6")
    draw.rectangle((190, 43, 224, 64), fill="#FFF0B8", outline=COLORS["wood_dark"])
    draw.text((194, 47), "NO BUGS", fill=COLORS["navy"], font=font_small)
    draw.text((198, 55), "TODAY", fill=COLORS["coral"], font=font_small)

    # Rug and furniture shadows.
    draw.ellipse((34, 119, 224, 135), fill="#BBD6DB")
    draw.ellipse((43, 121, 215, 133), fill="#C9E0E4")
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
    for x1, x2, y in ((49, 79, 92), (92, 132, 91), (151, 186, 93), (194, 216, 91)):
        draw.line((x1, y, x2, y), fill="#BA8041")
    draw.point((84, 93), fill="#7F522D")
    draw.point((188, 92), fill="#7F522D")

    # Notebook, pen, and mouse sit in the monitor's negative space.
    draw.polygon([(188, 81), (207, 80), (211, 88), (190, 89)], fill="#F6F0DD", outline=COLORS["navy_light"])
    draw.line((194, 83, 205, 82), fill="#B5B0A2")
    draw.line((195, 86, 207, 85), fill="#B5B0A2")
    draw.line((187, 79, 206, 88), fill=COLORS["coral"], width=2)
    draw.ellipse((214, 81, 221, 91), fill="#DCE7EA", outline=COLORS["navy_light"])
    draw.line((217, 83, 217, 86), fill=COLORS["navy_light"])


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
    draw.line((x + 2, y + 2, x + 59, y + 2), fill=COLORS["navy_light"])
    draw.line((x + 2, y + 2, x + 2, y + 45), fill=COLORS["navy_light"])
    draw.rectangle((x + 5, y + 5, x + 56, y + 39), fill=COLORS["screen"])
    draw.polygon([(x + 6, y + 6), (x + 24, y + 6), (x + 6, y + 24)], fill="#13334B")
    draw.rectangle((x + 28, y + 48, x + 34, y + 55), fill=COLORS["navy"])
    draw.rectangle((x + 18, y + 55, x + 44, y + 58), fill=COLORS["navy"])
    draw.rectangle((x + 7, y + 42, x + 9, y + 44), fill=COLORS["mint"])
    draw.arc((x + 51, y + 17, x + 72, y + 48), 265, 95, fill=COLORS["navy_light"], width=2)
    draw.rectangle((x + 65, y + 41, x + 70, y + 50), outline=COLORS["navy_light"])

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
    draw.line((122, 82, 168, 82), fill=COLORS["navy_light"])
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
        draw.line((114, 90, 119 + spread, 89), fill="#A86B4B")
        draw.point((126 + spread // 2, 96), fill=COLORS["coffee"])

    if stage == "error" and frame < 37:
        draw_spark(draw, 137, 80 - frame % 2, COLORS["yellow"], 3)
        draw_spark(draw, 154, 77 + frame % 2, COLORS["coral"], 2)


def draw_mug(draw: ImageDraw.ImageDraw, frame: int, stage: str) -> None:
    if stage in ("typing", "success"):
        draw.rectangle((104, 76, 114, 88), fill=COLORS["white"], outline=COLORS["navy"], width=1)
        draw.rectangle((105, 77, 107, 86), fill="#DDE9EC")
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
    draw.polygon([(75, 91), (84, 91), (79, 113), (72, 113)], fill=COLORS["denim"])
    draw.polygon([(87, 91), (97, 91), (104, 112), (96, 114)], fill=COLORS["navy"])
    draw.line((78, 93, 75, 109), fill=COLORS["denim_light"], width=2)
    draw.line((92, 93, 101, 109), fill=COLORS["navy_light"], width=2)
    draw.rectangle((68, 112, 80, 116), fill=COLORS["navy_dark"])
    draw.rectangle((97, 111, 111, 115), fill=COLORS["navy_dark"])
    draw.line((69, 116, 80, 116), fill="#8EA9B8")
    draw.line((98, 115, 111, 115), fill="#8EA9B8")

    # Hoodie with shading and drawstrings.
    draw.polygon([(70, 68), (91, 65), (101, 74), (98, 93), (68, 93)], fill=COLORS["mint"])
    draw.polygon([(68, 79), (75, 75), (77, 92), (68, 93)], fill="#42B99C")
    draw.polygon([(75, 69), (88, 66), (92, 70), (78, 75)], fill=COLORS["hoodie_light"])
    draw.line((78, 88, 94, 88), fill="#34A98E")
    draw.line((78, 88, 75, 91), fill="#34A98E")
    draw.line((94, 88, 97, 91), fill="#34A98E")
    draw.line((86, 68, 85, 78), fill=COLORS["white"], width=1)
    draw.line((91, 68, 92, 78), fill=COLORS["white"], width=1)
    draw.point((85, 79), fill=COLORS["navy"])
    draw.point((92, 79), fill=COLORS["navy"])

    # Head, ear, hair, and face.
    draw.rectangle((head_x, head_y, head_x + 16, head_y + 19), fill=COLORS["skin"])
    draw.rectangle((head_x + 2, head_y + 2, head_x + 5, head_y + 16), fill=COLORS["skin_light"])
    draw.rectangle((head_x + 14, head_y + 7, head_x + 16, head_y + 18), fill=COLORS["skin_shadow"])
    draw.rectangle((head_x - 2, head_y + 7, head_x + 1, head_y + 13), fill=COLORS["skin_shadow"])
    draw.polygon(
        [(head_x - 2, head_y + 1), (head_x + 4, head_y - 4), (head_x + 18, head_y - 2), (head_x + 18, head_y + 6), (head_x + 11, head_y + 4), (head_x + 6, head_y + 7), (head_x - 2, head_y + 7)],
        fill=COLORS["navy_dark"],
    )
    draw.rectangle((head_x + 5, head_y - 3, head_x + 13, head_y - 1), fill=COLORS["navy_light"])
    draw.point((head_x + 15, head_y + 13), fill=COLORS["skin_shadow"])

    screen_light = {
        "typing": COLORS["blue_light"],
        "success": COLORS["hoodie_light"],
        "spill": COLORS["hoodie_light"],
        "error": "#FF9A83",
        "recovery": "#9CB9C9",
    }[stage]
    draw.line((head_x + 16, head_y + 8, head_x + 16, head_y + 14), fill=screen_light)
    draw.line((97, 75, 98, 84), fill=screen_light, width=2)

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
    width, height = 1100, 180
    image = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype(r"C:\Windows\Fonts\Inkfree.ttf", 82)
    except OSError:
        font = ImageFont.truetype("DejaVuSans.ttf", 82)
    text = "Hey, I'm Dragon_xjy."
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    x = (width - text_width) // 2
    text_y = 24
    draw.text((x + 3, text_y + 4), text, font=font, fill=(24, 52, 79, 48))
    draw.text((x, text_y), text, font=font, fill=COLORS["navy"])

    underline_y = 132
    points = []
    for step in range(33):
        ratio = step / 32
        px = int(x + 48 + (text_width - 88) * ratio)
        py = int(underline_y + math.sin(ratio * math.pi) * 7 - math.sin(ratio * math.tau) * 2)
        points.append((px, py))
    draw.line(points, fill=COLORS["coral"], width=5)
    draw.line(points[4:-5], fill="#FF9A77", width=2)

    for sx, sy, color, size in (
        (x - 28, 72, COLORS["yellow"], 8),
        (x + text_width + 28, 52, COLORS["mint"], 7),
        (x + text_width + 8, 119, COLORS["coral"], 4),
    ):
        draw.line((sx - size, sy, sx + size, sy), fill=color, width=3)
        draw.line((sx, sy - size, sx, sy + size), fill=color, width=3)
        draw.ellipse((sx - 2, sy - 2, sx + 2, sy + 2), fill=COLORS["white"])
    image.save(output_dir / "dragonxjy-title.png", optimize=True)


def generate_cat_icon(output_dir: Path) -> None:
    palette_colors = (
        (0, 0, 0),
        (24, 52, 79),
        (245, 184, 77),
        (217, 134, 53),
        (255, 241, 205),
        (240, 139, 131),
        (89, 205, 177),
        (255, 255, 255),
        (245, 170, 145),
        (244, 119, 91),
    )
    palette = [channel for color in palette_colors for channel in color]
    palette.extend([0] * (768 - len(palette)))
    frames = []

    for frame in range(12):
        image = Image.new("P", (32, 32), 0)
        image.putpalette(palette)
        draw = ImageDraw.Draw(image)
        bob = -1 if frame in (2, 3, 8, 9) else 0
        tail_shift = int(round(math.sin(frame * math.tau / 12) * 2))

        draw.arc((2, 14 + tail_shift, 14, 29), 75, 275, fill=1, width=4)
        draw.arc((3, 14 + tail_shift, 13, 28), 75, 275, fill=3, width=2)
        draw.ellipse((8, 14 + bob, 24, 30 + bob), fill=1)
        draw.ellipse((10, 15 + bob, 22, 29 + bob), fill=2)
        draw.rectangle((11, 26 + bob, 14, 30 + bob), fill=3)
        draw.rectangle((19, 26 + bob, 22, 30 + bob), fill=3)

        draw.polygon([(7, 8 + bob), (9, 2 + bob), (14, 7 + bob)], fill=1)
        draw.polygon([(18, 7 + bob), (23, 2 + bob), (25, 10 + bob)], fill=1)
        draw.polygon([(9, 7 + bob), (10, 4 + bob), (13, 8 + bob)], fill=5)
        draw.polygon([(20, 8 + bob), (22, 4 + bob), (23, 9 + bob)], fill=5)
        draw.ellipse((6, 6 + bob, 25, 22 + bob), fill=1)
        draw.ellipse((8, 7 + bob, 23, 21 + bob), fill=2)
        draw.ellipse((11, 13 + bob, 21, 20 + bob), fill=4)

        if frame in (4, 5, 10):
            draw.line((11, 12 + bob, 14, 12 + bob), fill=1)
            draw.line((18, 12 + bob, 21, 12 + bob), fill=1)
        else:
            draw.rectangle((12, 11 + bob, 13, 13 + bob), fill=1)
            draw.rectangle((19, 11 + bob, 20, 13 + bob), fill=1)
            draw.point((12, 11 + bob), fill=7)
            draw.point((19, 11 + bob), fill=7)

        draw.polygon([(15, 15 + bob), (17, 15 + bob), (16, 17 + bob)], fill=5)
        draw.line((16, 17 + bob, 16, 18 + bob), fill=1)
        draw.line((16, 18 + bob, 14, 19 + bob), fill=1)
        draw.line((16, 18 + bob, 18, 19 + bob), fill=1)
        draw.point((10, 17 + bob), fill=8)
        draw.point((22, 17 + bob), fill=8)
        draw.line((10, 16 + bob, 4, 15 + bob), fill=1)
        draw.line((10, 18 + bob, 4, 19 + bob), fill=1)
        draw.line((22, 16 + bob, 28, 15 + bob), fill=1)
        draw.line((22, 18 + bob, 28, 19 + bob), fill=1)

        paw_y = 8 + (frame % 4 in (1, 2)) * 2
        draw.line((22, 20 + bob, 27, paw_y), fill=1, width=5)
        draw.line((22, 20 + bob, 27, paw_y), fill=2, width=3)
        draw.ellipse((25, paw_y - 2, 29, paw_y + 2), fill=2, outline=1)
        draw.rectangle((9, 19 + bob, 23, 21 + bob), fill=6)

        if frame in (7, 8, 9):
            draw.point((29, 3), fill=9)
            draw.point((28, 2), fill=9)
            draw.point((30, 2), fill=9)
            draw.point((29, 4), fill=9)

        frames.append(image.resize((96, 96), Image.Resampling.NEAREST))

    cat_path = output_dir / "waving-cat.gif"
    frames[0].save(
        cat_path,
        save_all=True,
        append_images=frames[1:],
        duration=110,
        loop=0,
        optimize=True,
        transparency=0,
        disposal=2,
    )


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
    generate_cat_icon(output_dir)
    print(f"Generated {gif_path} with {len(frames)} frames")


if __name__ == "__main__":
    main()
