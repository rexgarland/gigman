import os
from typing import List, Protocol

from .gitignore import Gitignore
from .section import TemplateSection
from .parse import parse_sections


def read_file(file: str) -> str:
    with open(file, "r") as f:
        text = f.read()
        return text


def write_file(file: str, text: str):
    with open(file, "w") as f:
        f.write(text)


class Manager(Protocol):
    def add_template(self, name: str, content: str):
        ...

    def remove_template(self, name: str):
        ...

    def save_gitignore(self):
        ...

    def get_existing_templates(self) -> List[str]:
        ...


class DirectoryManager:
    gitignore: Gitignore

    def __init__(self, folder):
        self.file = os.path.join(folder, ".gitignore")
        sections = []
        if os.path.exists(self.file):
            text = read_file(self.file)
            sections = parse_sections(text)
        self.gitignore = Gitignore(sections)

    def add_template(self, name, content):
        if not (name in self.get_existing_templates()):
            self.gitignore.add(TemplateSection(name, content))

    def remove_template(self, name):
        matching_name = lambda s: isinstance(s, TemplateSection) and s.name == name
        self.gitignore.remove(matching_name)

    def save_gitignore(self):
        text = str(self.gitignore)
        write_file(self.file, text)

    def get_existing_templates(self):
        return [
            s.name for s in self.gitignore.sections if isinstance(s, TemplateSection)
        ]
