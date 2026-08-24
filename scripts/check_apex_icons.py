#!/usr/bin/env python3
"""Validate the complete Apex icon set without third-party dependencies."""

from __future__ import annotations

import struct
import sys
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ICON_DIR = ROOT / "assets" / "images" / "apex"
EXPECTED = {"app", "length", "area", "volume", "mass", "speed", "temperature", "pressure", "time", "energy", "power"}
SIGNATURE = b"\x89PNG\r\n\x1a\n"


def inspect_png(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if not data.startswith(SIGNATURE):
        raise ValueError("invalid PNG signature")
    position = len(SIGNATURE)
    chunks: dict[bytes, list[bytes]] = {}
    while position < len(data):
        if position + 12 > len(data):
            raise ValueError("truncated chunk")
        length = struct.unpack(">I", data[position:position + 4])[0]
        kind = data[position + 4:position + 8]
        end = position + 12 + length
        if end > len(data):
            raise ValueError(f"truncated {kind.decode('ascii', 'replace')} chunk")
        payload = data[position + 8:position + 8 + length]
        expected_crc = struct.unpack(">I", data[position + 8 + length:end])[0]
        actual_crc = zlib.crc32(kind + payload) & 0xFFFFFFFF
        if actual_crc != expected_crc:
            raise ValueError(f"bad {kind.decode('ascii', 'replace')} CRC")
        chunks.setdefault(kind, []).append(payload)
        position = end
        if kind == b"IEND":
            break
    if position != len(data):
        raise ValueError("data found after IEND")
    if set((b"IHDR", b"PLTE", b"IDAT", b"IEND")) - chunks.keys():
        raise ValueError("missing required PNG chunk")
    if len(chunks[b"IHDR"]) != 1 or len(chunks[b"PLTE"]) != 1 or len(chunks[b"IEND"]) != 1:
        raise ValueError("invalid singleton chunk count")
    width, height, depth, color_type, compression, filtering, interlace = struct.unpack(">IIBBBBB", chunks[b"IHDR"][0])
    if (width, height) != (32, 32):
        raise ValueError(f"expected 32x32, found {width}x{height}")
    if (depth, color_type) != (8, 3):
        raise ValueError(f"expected 8-bit indexed color type 3, found depth={depth} type={color_type}")
    if (compression, filtering, interlace) != (0, 0, 0):
        raise ValueError("unsupported PNG encoding flags")
    palette = chunks[b"PLTE"][0]
    if not palette or len(palette) % 3 or len(palette) > 256 * 3:
        raise ValueError("invalid palette length")
    entries = len(palette) // 3
    alpha = chunks.get(b"tRNS", [b""])[0]
    if not alpha or len(alpha) > entries or alpha[0] != 0:
        raise ValueError("palette index zero must be transparent")
    packed = zlib.decompress(b"".join(chunks[b"IDAT"]))
    if len(packed) != height * (width + 1):
        raise ValueError("unexpected inflated image length")
    used: set[int] = set()
    for y in range(height):
        row = packed[y * (width + 1):(y + 1) * (width + 1)]
        if row[0] != 0:
            raise ValueError("generator output must use deterministic unfiltered scanlines")
        used.update(row[1:])
    if max(used) >= entries:
        raise ValueError("pixel references a missing palette entry")
    if 0 not in used or len(used) < 4:
        raise ValueError("icon must contain transparency and at least three visible colors")
    corner_indices = [packed[1], packed[width], packed[(height - 1) * (width + 1) + 1], packed[-1]]
    if any(index != 0 for index in corner_indices):
        raise ValueError("all four icon corners must be transparent")
    return entries, len(used)


def main() -> int:
    actual = {path.stem for path in ICON_DIR.glob("*.png")}
    missing, extra = sorted(EXPECTED - actual), sorted(actual - EXPECTED)
    errors: list[str] = []
    if missing:
        errors.append(f"missing icons: {', '.join(missing)}")
    if extra:
        errors.append(f"unexpected icons: {', '.join(extra)}")
    for name in sorted(EXPECTED & actual):
        try:
            entries, used = inspect_png(ICON_DIR / f"{name}.png")
            print(f"ok  {name:11} 32x32 indexed, {used} used/{entries} palette colors")
        except (OSError, ValueError, struct.error, zlib.error) as error:
            errors.append(f"{name}.png: {error}")
    if errors:
        print("Apex icon validation failed:", file=sys.stderr)
        for error in errors:
            print(f"  {error}", file=sys.stderr)
        return 1
    print(f"Validated all {len(EXPECTED)} Apex icons.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
