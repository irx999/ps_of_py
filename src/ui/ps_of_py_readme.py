import os
import sys

from src.ui.utils import st_markdown

if __name__ == "__main__":
    possible_paths = [
        "plugins/ps_of_py/README.md",
        f"{sys._MEIPASS}/plugins/ps_of_py/README.md",  # type: ignore
    ]

    for path in possible_paths:
        if os.path.exists(path):
            FILE_PATH = path
            break

    with open(FILE_PATH, "r", encoding="utf-8") as f:
        readme_text = f.read()

        st_markdown(readme_text)
