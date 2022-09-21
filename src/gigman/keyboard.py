from enum import Enum, auto
import sys
from typing import Optional, Protocol


class Event(Protocol):
    type: str
    value: Optional[str]


class KeyPress:
    type = "key"

    def __init__(self, key):
        self.value = key


class Direction(str, Enum):
    UP = auto()
    DOWN = auto()
    RIGHT = auto()
    LEFT = auto()


DIRECTION_CHARS = {
    "A": Direction.UP,
    "B": Direction.DOWN,
    "C": Direction.RIGHT,
    "D": Direction.LEFT,
}


def direction_from_char(d: str) -> Direction:
    assert d in DIRECTION_CHARS, "Unknown arrow key"
    return DIRECTION_CHARS[d]


class ArrowPress:
    type = "arrow"

    def __init__(self, direction: Direction):
        self.value = direction


class Keyboard(Protocol):
    """Reads keyboard events"""

    def read_event(self) -> Event:
        ...


class TerminalKeyboard:
    def read_event(self) -> Event:
        char = sys.stdin.read(1)
        if char == "\x1b":
            sys.stdin.read(1)
            direction = sys.stdin.read(1)
            return ArrowPress(direction_from_char(direction))
        return KeyPress(char)
