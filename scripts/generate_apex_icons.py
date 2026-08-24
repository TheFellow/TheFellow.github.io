#!/usr/bin/env python3
"""Deterministically draw Apex's 32px indexed-color icon set."""

from __future__ import annotations

import struct
import zlib
from pathlib import Path

SIZE = 32
OUTPUT = Path(__file__).resolve().parents[1] / "assets" / "images" / "apex"
TRANSPARENT = (0, 0, 0, 0)

# Compact, saturated ramps evoke hand-drawn 256-color Windows shareware art.
K = (24, 18, 38, 255)
INK = (42, 48, 67, 255)
WHITE = (255, 255, 246, 255)
SILVER = (205, 215, 224, 255)
GRAY = (105, 115, 132, 255)
BLUE = (26, 76, 184, 255)
CYAN = (54, 218, 246, 255)
NAVY = (16, 34, 112, 255)
RED = (217, 35, 60, 255)
PINK = (255, 116, 139, 255)
YELLOW = (255, 231, 55, 255)
GOLD = (241, 151, 25, 255)
ORANGE = (255, 91, 25, 255)
GREEN = (27, 176, 76, 255)
LIME = (136, 240, 71, 255)
PURPLE = (128, 48, 195, 255)
VIOLET = (218, 89, 241, 255)
BROWN = (120, 67, 34, 255)


class Canvas:
    def __init__(self) -> None:
        self.pixels = [[TRANSPARENT for _ in range(SIZE)] for _ in range(SIZE)]

    def pixel(self, x: int, y: int, color: tuple[int, int, int, int]) -> None:
        if 0 <= x < SIZE and 0 <= y < SIZE:
            self.pixels[y][x] = color

    def rect(self, box: tuple[int, int, int, int], color: tuple[int, int, int, int]) -> None:
        x0, y0, x1, y1 = box
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.pixel(x, y, color)

    def polygon(self, points: list[tuple[int, int]], color: tuple[int, int, int, int]) -> None:
        # Scan at pixel centers. Horizontal edges use the conventional half-open rule.
        for y in range(SIZE):
            intersections: list[float] = []
            scan = y + 0.5
            for index, (x1, y1) in enumerate(points):
                x2, y2 = points[(index + 1) % len(points)]
                if (y1 <= scan < y2) or (y2 <= scan < y1):
                    intersections.append(x1 + (scan - y1) * (x2 - x1) / (y2 - y1))
            intersections.sort()
            for left, right in zip(intersections[::2], intersections[1::2]):
                for x in range(int(left + 0.5), int(right + 0.5)):
                    self.pixel(x, y, color)

    def line(self, start: tuple[int, int], end: tuple[int, int], color: tuple[int, int, int, int], width: int = 1) -> None:
        x0, y0 = start
        x1, y1 = end
        dx, sx = abs(x1 - x0), 1 if x0 < x1 else -1
        dy, sy = -abs(y1 - y0), 1 if y0 < y1 else -1
        error = dx + dy
        radius = width // 2
        while True:
            self.rect((x0 - radius, y0 - radius, x0 + radius, y0 + radius), color)
            if x0 == x1 and y0 == y1:
                break
            twice = 2 * error
            if twice >= dy:
                error += dy
                x0 += sx
            if twice <= dx:
                error += dx
                y0 += sy

    def ellipse(self, box: tuple[int, int, int, int], color: tuple[int, int, int, int]) -> None:
        x0, y0, x1, y1 = box
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        rx, ry = max((x1 - x0 + 1) / 2, 0.5), max((y1 - y0 + 1) / 2, 0.5)
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1:
                    self.pixel(x, y, color)


def bolt(c: Canvas, offset: int = 0) -> None:
    outline = [(16, 1 + offset), (27, 1 + offset), (21, 11 + offset), (29, 11 + offset),
               (10, 31 + offset), (14, 18 + offset), (5, 18 + offset)]
    fill = [(17, 4 + offset), (23, 4 + offset), (17, 14 + offset), (24, 14 + offset),
            (13, 25 + offset), (16, 16 + offset), (9, 16 + offset)]
    c.polygon(outline, K)
    c.polygon(fill, GOLD)
    c.polygon([(17, 4 + offset), (20, 4 + offset), (15, 15 + offset), (10, 15 + offset)], YELLOW)
    c.line((17, 5 + offset), (10, 15 + offset), WHITE)
    c.line((17, 28 + offset), (26, 15 + offset), ORANGE)


def draw_app() -> Canvas:
    c = Canvas(); bolt(c); return c


def draw_length() -> Canvas:
    c = Canvas()
    c.polygon([(3, 22), (20, 4), (29, 12), (11, 29)], K)
    c.polygon([(5, 21), (20, 7), (27, 12), (11, 27)], GOLD)
    c.polygon([(7, 20), (20, 8), (22, 10), (9, 23)], YELLOW)
    for p, q in [((18, 9), (21, 12)), ((14, 13), (18, 17)), ((10, 17), (13, 20)), ((22, 10), (24, 12))]:
        c.line(p, q, BROWN, 1)
    c.line((7, 24), (12, 27), ORANGE); return c


def draw_area() -> Canvas:
    c = Canvas()
    c.rect((3, 3, 28, 28), K); c.rect((5, 5, 26, 26), BLUE)
    colors = [CYAN, VIOLET, PINK, GOLD]
    for row in range(4):
        for col in range(4):
            color = colors[(row + col) % len(colors)]
            c.rect((6 + col * 5, 6 + row * 5, 9 + col * 5, 9 + row * 5), color)
            c.pixel(6 + col * 5, 6 + row * 5, WHITE)
    c.line((5, 27), (27, 5), WHITE); return c


def draw_volume() -> Canvas:
    c = Canvas()
    c.polygon([(4, 4), (23, 4), (21, 28), (8, 28)], K)
    c.polygon([(7, 7), (20, 7), (19, 25), (10, 25)], SILVER)
    c.polygon([(9, 15), (19, 15), (18, 25), (10, 25)], CYAN)
    c.line((10, 17), (18, 17), WHITE); c.line((11, 20), (18, 20), BLUE)
    c.line((17, 10), (21, 10), GRAY); c.line((17, 13), (20, 13), GRAY)
    c.ellipse((19, 8, 30, 21), K); c.ellipse((21, 10, 27, 18), TRANSPARENT)
    c.line((22, 19), (19, 21), K, 2); return c


def draw_mass() -> Canvas:
    c = Canvas()
    c.line((16, 4), (16, 24), K, 3); c.line((6, 9), (26, 9), K, 3)
    c.polygon([(4, 11), (12, 11), (10, 21), (6, 21)], GOLD)
    c.polygon([(20, 11), (28, 11), (26, 21), (22, 21)], GOLD)
    c.line((8, 10), (5, 18), WHITE); c.line((24, 10), (21, 18), WHITE)
    c.rect((10, 24, 22, 27), K); c.rect((7, 28, 25, 30), K)
    c.rect((12, 24, 20, 25), SILVER); return c


def draw_speed() -> Canvas:
    c = Canvas()
    c.ellipse((2, 2, 29, 29), K); c.ellipse((5, 5, 26, 26), BLUE); c.ellipse((8, 8, 23, 23), WHITE)
    for angle_point in [(9, 20), (8, 14), (12, 9), (18, 8), (23, 12), (24, 18)]:
        c.line((16, 16), angle_point, GRAY)
    c.ellipse((11, 11, 21, 21), WHITE)
    c.line((16, 16), (23, 9), RED, 2); c.ellipse((13, 13, 18, 18), K)
    c.pixel(15, 14, PINK); return c


def draw_temperature() -> Canvas:
    c = Canvas()
    c.ellipse((8, 20, 23, 31), K); c.rect((10, 4, 21, 25), K)
    c.ellipse((12, 6, 19, 13), WHITE); c.rect((12, 10, 19, 24), WHITE)
    c.rect((15, 11, 18, 25), RED); c.ellipse((11, 21, 21, 29), RED)
    c.rect((12, 9, 14, 19), CYAN); c.pixel(13, 8, WHITE)
    for y in (12, 16, 20): c.line((20, y), (24, y), K)
    return c


def draw_pressure() -> Canvas:
    c = Canvas()
    c.ellipse((2, 2, 29, 29), K); c.ellipse((5, 5, 26, 26), GOLD); c.ellipse((8, 8, 23, 23), WHITE)
    for p in [(9, 18), (10, 12), (15, 9), (21, 11), (23, 17)]: c.line((16, 16), p, GRAY)
    c.ellipse((11, 11, 21, 21), WHITE); c.line((16, 16), (9, 10), PURPLE, 2)
    c.ellipse((13, 13, 18, 18), K); c.rect((11, 25, 20, 30), K); c.rect((13, 25, 18, 29), SILVER)
    return c


def draw_time() -> Canvas:
    c = Canvas()
    c.ellipse((2, 2, 29, 29), K); c.ellipse((5, 5, 26, 26), CYAN); c.ellipse((8, 8, 23, 23), WHITE)
    c.rect((14, 6, 17, 9), NAVY); c.rect((14, 22, 17, 25), NAVY)
    c.rect((6, 14, 9, 17), NAVY); c.rect((22, 14, 25, 17), NAVY)
    c.line((16, 16), (16, 9), BLUE, 2); c.line((16, 16), (21, 19), RED, 2)
    c.ellipse((13, 13, 18, 18), K); c.pixel(15, 14, WHITE); return c


def draw_energy() -> Canvas:
    c = Canvas()
    # Radiant atom: three colored electron orbits around a hot nucleus.
    c.ellipse((5, 11, 26, 20), BLUE); c.ellipse((7, 13, 24, 18), TRANSPARENT)
    c.polygon([(8, 5), (11, 4), (24, 25), (21, 27)], PURPLE)
    c.polygon([(10, 7), (11, 7), (22, 25), (21, 25)], TRANSPARENT)
    c.polygon([(22, 5), (25, 7), (10, 27), (7, 24)], GREEN)
    c.polygon([(23, 7), (24, 8), (9, 25), (9, 24)], TRANSPARENT)
    c.ellipse((11, 11, 20, 20), K); c.ellipse((13, 13, 18, 18), ORANGE); c.pixel(14, 14, YELLOW)
    c.ellipse((4, 13, 8, 17), CYAN); c.ellipse((21, 4, 25, 8), VIOLET); c.ellipse((21, 23, 25, 27), LIME)
    return c


def draw_power() -> Canvas:
    c = Canvas()
    c.polygon([(6, 3), (22, 3), (27, 8), (27, 20), (22, 25), (6, 25), (3, 20), (3, 8)], K)
    c.polygon([(8, 6), (20, 6), (24, 10), (24, 18), (20, 22), (8, 22), (6, 18), (6, 10)], PURPLE)
    c.ellipse((9, 9, 20, 20), VIOLET); c.ellipse((12, 12, 17, 17), K)
    c.rect((9, 23, 13, 29), K); c.rect((18, 23, 22, 29), K)
    c.rect((10, 23, 11, 28), SILVER); c.rect((19, 23, 20, 28), SILVER)
    c.polygon([(15, 7), (20, 7), (17, 13), (21, 13), (13, 22), (15, 15), (11, 15)], YELLOW)
    c.pixel(16, 8, WHITE); return c


ICONS = {
    "app": draw_app,
    "length": draw_length,
    "area": draw_area,
    "volume": draw_volume,
    "mass": draw_mass,
    "speed": draw_speed,
    "temperature": draw_temperature,
    "pressure": draw_pressure,
    "time": draw_time,
    "energy": draw_energy,
    "power": draw_power,
}


def chunk(kind: bytes, payload: bytes) -> bytes:
    return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF)


def encode(canvas: Canvas) -> bytes:
    colors = [TRANSPARENT]
    for row in canvas.pixels:
        for color in row:
            if color not in colors:
                colors.append(color)
    if len(colors) > 256:
        raise ValueError(f"icon needs {len(colors)} palette entries")
    indices = {color: index for index, color in enumerate(colors)}
    scanlines = b"".join(b"\x00" + bytes(indices[color] for color in row) for row in canvas.pixels)
    palette = b"".join(bytes(color[:3]) for color in colors)
    alpha = bytes(color[3] for color in colors)
    signature = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", SIZE, SIZE, 8, 3, 0, 0, 0)
    return signature + chunk(b"IHDR", ihdr) + chunk(b"PLTE", palette) + chunk(b"tRNS", alpha) + chunk(b"IDAT", zlib.compress(scanlines, 9)) + chunk(b"IEND", b"")


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for name, draw in ICONS.items():
        path = OUTPUT / f"{name}.png"
        path.write_bytes(encode(draw()))
        print(path.relative_to(OUTPUT.parents[2]))


if __name__ == "__main__":
    main()
