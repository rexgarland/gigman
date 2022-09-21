from typing import Protocol
from enum import Enum
import uuid
import time


class LogLevel(Enum):
    DEBUG = "debug"
    INFO = "info"
    WARN = "warn"
    ERROR = "error"

    @property
    def number(self):
        return ["debug", "info", "warn", "error"].index(self.value)


class Logger(Protocol):
    level: LogLevel

    def log(self, message: str, level: LogLevel = LogLevel.INFO):
        ...


def rightpad(string: str, length: int) -> str:
    to_pad = max(0, length - len(string))
    return string + " " * to_pad


def get_fixed_width_timestamp():
    seconds = time.time()
    return rightpad(str(seconds)[:15], 15)


class FileLogger:
    def __init__(self, file, level=LogLevel.INFO):
        self.level = level
        self.file = file
        self.session = str(uuid.uuid4())[:4]

    def log(self, message, level=LogLevel.INFO):
        if level.number >= self.level.number:
            timestamp = get_fixed_width_timestamp()
            with open(self.file, "a") as f:
                f.write(f"[{self.session}] [{timestamp}] [{level.value}]: {message}\n")
