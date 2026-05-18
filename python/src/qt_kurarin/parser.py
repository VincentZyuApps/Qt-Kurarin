from __future__ import annotations

import math
from pathlib import Path

from .animation import Movement, SpriteDefinition, SENTINEL_END


def normalize_resource_name(raw_path: str) -> str:
    stripped = raw_path.strip().strip('"')
    return stripped.replace("\\", "_")


def parse_float(value: str, default: float = math.nan) -> float:
    value = value.strip()
    if not value:
        return default
    try:
        return float(value)
    except ValueError:
        return default


def parse_int(value: str, default: int) -> int:
    value = value.strip()
    if not value:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def parse_movements(block_lines: list[str]) -> list[Movement]:
    result: list[Movement] = []
    for raw_line in block_lines:
        line = raw_line.strip()
        if not line:
            continue
        parts = [part.strip() for part in line.split(",")]
        if not parts:
            continue

        movement = Movement()
        movement.type = parts[0]

        if movement.type in {"S", "F"}:
            movement.move_from = 1
            movement.move_end = 1

        if len(parts) > 1:
            movement.easing = parse_int(parts[1], 0)
        if len(parts) > 2:
            movement.time_start = parse_int(parts[2], 0)
        if len(parts) > 3:
            movement.time_end = parse_int(parts[3], SENTINEL_END)
        if len(parts) > 4:
            movement.move_from = parse_float(parts[4], 0)
        if len(parts) > 5:
            movement.move_end = parse_float(parts[5], math.nan)
        if len(parts) > 6:
            movement.sub_value = parse_float(parts[6], math.nan)
        if len(parts) > 7:
            movement.sub_value2 = parse_float(parts[7], math.nan)

        if math.isnan(movement.move_from):
            if movement.type in {"S", "F"}:
                movement.move_from = 1
            elif movement.type in {"MX", "MY"}:
                movement.move_from = 0

        if len(parts) == 5 and movement.type in {"MX", "MY", "S", "F"}:
            movement.move_end = movement.move_from

        result.append(movement)
    return result


def parse_script(script_path: Path) -> tuple[list[SpriteDefinition], int]:
    sprites: list[SpriteDefinition] = []
    max_time = 0

    current_header: str | None = None
    current_block: list[str] = []

    def flush() -> None:
        nonlocal current_header, current_block, max_time
        if not current_header:
            return
        parts = [part.strip() for part in current_header.split(",")]
        if len(parts) < 6:
            current_header = None
            current_block = []
            return

        resource_name = normalize_resource_name(parts[3])
        x = parse_float(parts[4], 0)
        y = parse_float(parts[5], 0)
        movements = parse_movements(current_block)
        for movement in movements:
            max_time = max(max_time, movement.time_start)
            if movement.time_end != SENTINEL_END:
                max_time = max(max_time, movement.time_end)
        sprites.append(
            SpriteDefinition(
                resource_name=resource_name,
                x=x,
                y=y,
                movements=movements,
            )
        )
        current_header = None
        current_block = []

    for raw_line in script_path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip():
            continue
        if not raw_line.startswith(" "):
            flush()
            current_header = raw_line
            current_block = []
        else:
            current_block.append(raw_line)

    flush()
    return sprites, max_time
