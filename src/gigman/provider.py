import os
from importlib_resources import files
from functools import lru_cache
from typing import List, Optional, Protocol

from .template import Template


class Provider(Protocol):
    def get_options(self) -> List[str]:
        ...

    def get_template(self, name: str) -> Optional[Template]:
        ...


class GithubTemplatesProvider:
    repo = files("gigman").joinpath("data")

    @lru_cache
    def get_options(self) -> List[str]:
        suffix = ".gitignore"
        files = self.repo.iterdir()
        filtered_files = [file for file in files if file.name.endswith(suffix)]
        names = [file.name[: -len(suffix)] for file in filtered_files]
        return names

    def get_template(self, name: str) -> Optional[Template]:
        file = self.repo.joinpath(name + ".gitignore")
        if file.is_file():
            text = file.read_text()
            return Template(name, text)
        return None
