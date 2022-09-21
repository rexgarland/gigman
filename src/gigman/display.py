import sys
import termios
import tty
from typing import Protocol


class Display(Protocol):
    def print(self, text: str):
        ...

    def seek(self, x: int, y: int):
        ...


class Terminal:
    def __init__(self):
        self.fd = sys.stdout.fileno()
        self.old_settings = termios.tcgetattr(self.fd)
        self.y = 0
        self.y_max = 0

    def __enter__(self):
        tty.setraw(sys.stdout)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        tty.setraw(sys.stdout)
        termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)

    def clear_line(self):
        self.write("\u001b[2K")

    def clear(self):
        for y in range(self.y_max, -1, -1):
            self.seek(0, y)
            self.clear_line()

    def write(self, text: str):
        lines = text.split("\n")
        sys.stdout.write("\n\u001b[1000D".join(lines))
        self.y += text.count("\n")
        self.y_max = max(self.y_max, self.y)
        sys.stdout.flush()

    def seek(self, x, y):
        # move the terminal cursor to an absolute position
        # (0,0) is the top left
        if y > self.y_max:
            self.seek(0, self.y_max)
            dy = y - self.y_max
            self.write("\n" * dy)
            self.seek(x, y)
        if y < self.y:
            dy = y - self.y
            self.write(f"\u001b[{-dy}A")
            self.y = y
        elif y > self.y:
            dy = y - self.y
            self.write(f"\u001b[{dy}B")
            self.y = y
        self.write("\u001b[1000D")
        if x > 0:
            self.write(f"\u001b[{x}C")

    def print(self, text):
        self.clear()
        self.write(text)
