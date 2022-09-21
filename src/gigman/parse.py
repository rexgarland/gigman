from typing import Optional
from .section import PREFIX, SUFFIX, TemplateSection, TextSection, Section


def is_template_start(line):
    return line.startswith(PREFIX)


def is_template_end(line):
    return line.startswith(SUFFIX)


def get_template_name(line):
    return line.split(":")[-1].strip()


class Parser:
    buffer: list[str]
    currently_in: Optional[str] = None

    def __init__(self, handle_new_section):
        self.report_new_section = handle_new_section
        self.buffer = []

    def feed(self, line):
        if is_template_start(line):
            if self.buffer:
                self.report_new_section(TextSection("\n".join(self.buffer)))
                self.buffer = []
            name = get_template_name(line)
            self.currently_in = name
        elif is_template_end(line) and get_template_name(line) == self.currently_in:
            content = "\n".join(self.buffer)
            self.report_new_section(TemplateSection(self.currently_in, content))
            self.buffer = []
            self.currently_in = None
        else:
            self.buffer.append(line)

    def end(self):
        if self.buffer:
            self.report_new_section(TextSection("\n".join(self.buffer)))


def parse_sections(text: str) -> list[Section]:
    sections = []
    lines = text.split("\n")

    parser = Parser(lambda s: sections.append(s))
    for line in lines:
        parser.feed(line)
    parser.end()

    return sections
