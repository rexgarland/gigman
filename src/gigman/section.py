from typing import Protocol

PREFIX = "## gigman[start]: "
SUFFIX = "## gigman[end]: "


class Section(Protocol):
    content: str

    def __str__(self) -> str:
        ...


class TextSection:
    def __init__(self, content):
        self.content = content

    def __str__(self):
        return self.content


class TemplateSection:
    def __init__(self, name, content):
        self.content = content
        self.name = name

    def __str__(self):
        prefix = PREFIX + self.name
        suffix = SUFFIX + self.name
        wrapped_content = "\n\n".join([prefix, self.content, suffix])
        return wrapped_content
