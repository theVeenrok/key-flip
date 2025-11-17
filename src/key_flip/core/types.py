import enum
from typing import NewType, TypeAlias

LayoutId = NewType("LayoutId", str)
LayoutPairId = NewType("LayoutPairId", str)
Char: TypeAlias = str


class Direction(enum.StrEnum):
    FORWARD = "forward"
    BACKWARD = "backward"
