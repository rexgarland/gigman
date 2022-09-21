from typing import Optional

from .manager import DirectoryManager
from .ui import UI
from .display import Terminal
from .logger import LogLevel, Logger
from .keyboard import ArrowPress, KeyPress, TerminalKeyboard
from .provider import GithubTemplatesProvider



class App:
    """Runs the terminal application"""

    def __init__(self, folder=".", logger: Optional[Logger] = None):
        self.folder = folder
        self.logger = logger

    def log(self, message, level: LogLevel = LogLevel.INFO):
        if self.logger:
            self.logger.log(message, level)

    def run(self):
        self.log("started running app...")
        self.log("started initializing provider...")
        provider = GithubTemplatesProvider()
        self.log("...finished initializing provider")
        manager = DirectoryManager(self.folder)

        keyboard = TerminalKeyboard()

        with Terminal() as display:
            self.ui = UI(provider, manager, display)
            while True:
                event = keyboard.read_event()
                self.log(f"event received: {event}", level=LogLevel.DEBUG)

                if isinstance(event, KeyPress):
                    char = event.value
                    self.log(
                        f"read {repr(char)} (ord {ord(char)})", level=LogLevel.DEBUG
                    )

                    if ord(event.value) == 3:  # Ctrl-C
                        self.log("...finished running app")
                        break

                elif isinstance(event, ArrowPress):
                    direction = event.value
                    self.log(f"read arrow key {repr(direction)}")

                self.ui.handle(event)
                self.log(f"query = '{self.ui.query}'", level=LogLevel.DEBUG)
