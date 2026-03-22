import streamlit as st

from src.ui.utils import get_path2

pages = {
    "🎨PS自动化": [
        st.Page(
            get_path2(__file__, "main.py"),
            title="主界面",
            icon="🎨",
        ),
        st.Page(
            get_path2(__file__, "ps_of_py_readme.py"),
            title="README.md",
            icon="📄",
        ),
        st.Page(
            get_path2(__file__, "ps_of_py_changelog.py"),
            title="CHANGELOG.md",
            icon="🔄",
        ),
    ]
}

__all__ = [
    "pages",
]
