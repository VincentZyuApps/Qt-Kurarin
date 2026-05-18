from __future__ import annotations

from dataclasses import dataclass, field


SENTINEL_END = -(2**31)


@dataclass(slots=True)
class Movement:
    type: str = ""
    easing: int = 0
    time_start: int = 0
    time_end: int = SENTINEL_END
    move_from: float = 0.0
    move_end: float = 0.0
    sub_value: float = float("nan")
    sub_value2: float = float("nan")

    @property
    def is_instant(self) -> bool:
        return self.time_end == SENTINEL_END


@dataclass(slots=True)
class SpriteDefinition:
    resource_name: str
    x: float
    y: float
    movements: list[Movement] = field(default_factory=list)


@dataclass(slots=True)
class SpriteState:
    x: float
    y: float
    opacity: float = 1.0
    scale: float = 1.0
