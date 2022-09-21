from dataclasses import dataclass
from typing import Set

from .display import Display
from .keyboard import Event, KeyPress
from .manager import Manager
from .provider import Provider


PROMPT = "Add templates to your gitignore...\n> "
SELECTED_CHAR = "●"
DESELECTED_CHAR = "○"


class TemplateSelection(Set[str]):
    def includes(self, name: str):
        return any([t == name for t in self])


MAX_DISPLAYED_LINES = 6


@dataclass
class UIState:
    query: str = ""
    scroll: int = 0


class UI:
    """Handles user events"""

    def __init__(self, provider: Provider, manager: Manager, display: Display):
        self.provider = provider
        self.manager = manager
        self.display = display
        self.state = UIState()
        self.formatter = UIFormatter()
        self.update()

    @property
    def query(self):
        return self.state.query

    @property
    def selections(self):
        return [
            opt
            for opt in self.provider.get_options()
            if opt in self.manager.get_existing_templates()
        ]

    @property
    def filtered_options(self) -> list[str]:
        return [
            opt
            for opt in sorted(self.provider.get_options())
            if opt.startswith(self.state.query)
        ]

    def update(self):
        text, position = self.formatter.format(self)
        self.display.print(text)
        self.display.seek(*position)

    def handle_key_press(self, key):
        self.state.query += key
        self.update()

    def handle_backspace(self):
        self.state.query = self.query[:-1]
        self.update()

    def handle_select(self):
        if len(self.state.query) > 0 and len(self.filtered_options) > 0:
            name = self.filtered_options[0]
            if name in self.manager.get_existing_templates():
                self.manager.remove_template(name)
            else:
                template = self.provider.get_template(name)
                if template:
                    self.manager.add_template(name, template.text)
            self.manager.save_gitignore()
        self.update()

    def handle(self, event: Event):
        if isinstance(event, KeyPress):
            key = event.value
            if key in ["\t", " ", "\r"]:
                self.handle_select()
            elif key == "\x7f":
                self.handle_backspace()
            else:
                self.handle_key_press(key)


class UIFormatter:
    """Formats UI state for display"""

    def get_text_output(self, ui: UI):
        options = [opt for opt in ui.filtered_options]

        if len(ui.query) > 0 and len(options) > 0:
            query = options[0]
            options = options[1:]
            query_mark = (
                SELECTED_CHAR
                if query in ui.manager.get_existing_templates()
                else DESELECTED_CHAR
            )
        else:
            query = ui.query
            query_mark = " "

        if len(options) > MAX_DISPLAYED_LINES:
            options = options[:MAX_DISPLAYED_LINES] + ["..."]

        annotated_options = [
            " "
            + (
                SELECTED_CHAR
                if option in ui.manager.get_existing_templates()
                else DESELECTED_CHAR
            )
            + " "
            + option
            for option in options
        ]
        text = "\n".join([">" + query_mark + " " + query] + annotated_options)

        return text

    def format(self, ui: UI):
        cursor = (3 + len(ui.query), 0)

        text = self.get_text_output(ui)

        return text, cursor
