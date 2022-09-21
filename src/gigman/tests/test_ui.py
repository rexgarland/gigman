"""
The UI handles user events.
"""


from typing import Optional
from tempfile import TemporaryDirectory

from ..manager import DirectoryManager, Manager
from ..template import Template
from ..ui import UI
from ..keyboard import KeyPress


class DummyTemplateProvider:
    def get_options(self):
        return ["Node", "Python"]

    def get_template(self, name):
        return Template(name, "")


class DummyGitignoreManager:
    def __init__(self):
        self.templates = []

    def add_template(self, name: str, content: str):
        self.templates.append(Template(name, content))

    def remove_template(self, name: str):
        self.templates = [t for t in self.templates if t.name != name]

    def save_gitignore(self):
        pass

    def get_existing_templates(self):
        return [t.name for t in self.templates]


class DummyDisplay:
    def print(self, text):
        pass

    def seek(self, x, y):
        pass


class DummyUIFactory:
    def create_ui(self, manager: Optional[Manager] = None):
        provider = DummyTemplateProvider()
        manager = manager if manager else DummyGitignoreManager()
        display = DummyDisplay()
        return UI(provider, manager, display)


ui_factory = DummyUIFactory()


def test_should_update_local_gitignore():
    with TemporaryDirectory() as tmpdir:
        before = ""
        local_manager = DirectoryManager(tmpdir)
        ui = ui_factory.create_ui(manager=local_manager)
        ui.handle(KeyPress("P"))
        ui.handle(KeyPress("\r"))
        after = ""
        with open(tmpdir + "/.gitignore", "r") as f:
            after = f.read()
        assert before != after, "UI did not change gitignore"


def test_should_not_select_when_query_empty():
    ui = ui_factory.create_ui()
    ui.handle(KeyPress("\t"))
    assert ui.selections == []


def test_should_replace_options_on_clear_filter():
    ui = ui_factory.create_ui()
    ui.handle(KeyPress("P"))
    ui.handle(KeyPress("\x7f"))
    assert "Node" in ui.filtered_options


def test_should_remove_char_on_backspace():
    ui = ui_factory.create_ui()
    ui.handle(KeyPress("P"))
    ui.handle(KeyPress("\x7f"))
    assert ui.query == ""


def test_handles_return_selection():
    ui = ui_factory.create_ui()
    ui.handle(KeyPress("P"))
    ui.handle(KeyPress("\r"))
    assert "Python" in ui.selections


def test_handles_space_selection():
    ui = ui_factory.create_ui()
    ui.handle(KeyPress("P"))
    ui.handle(KeyPress(" "))
    assert "Python" in ui.selections


def test_handles_tab_selection():
    ui = ui_factory.create_ui()
    ui.handle(KeyPress("P"))
    ui.handle(KeyPress("\t"))
    assert "Python" in ui.selections


def test_should_filter_options():
    ui = ui_factory.create_ui()
    ui.handle(KeyPress("P"))
    assert not ("Node" in ui.filtered_options)


def test_ui_should_update_query_on_key_press():
    ui = ui_factory.create_ui()
    event = KeyPress("P")
    ui.handle(event)
    assert ui.query == "P"
