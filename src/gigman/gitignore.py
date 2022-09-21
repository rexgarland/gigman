from typing import Callable
from .section import Section, TemplateSection


class Gitignore:
    def __init__(self, sections):
        self.sections = sections

    def add(self, section: Section):
        self.sections.append(section)

    def remove(self, predicate: Callable[[Section], bool]):
        self.sections = [s for s in self.sections if not predicate(s)]

    def __str__(self):
        blocks = [str(section).strip() for section in self.sections]
        return "\n\n".join(blocks)
