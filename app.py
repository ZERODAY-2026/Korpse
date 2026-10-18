"""Korpse - Private Legal Document Triage Agent (Streamlit entry point)."""

import streamlit as st

from config import USE_STUB

if USE_STUB:
    from core import stub_backend as backend
else:
    # TODO: import the real backend once Shiven confirms its module and
    # functions in INTEGRATION_CONTRACT.md. Do not guess the import.
    raise NotImplementedError("The real backend is not connected yet. Set USE_STUB = True in config.py.")

from ui.about import render_about
from ui.chat import render_chat
from ui.review import render_review
from ui.sidebar import render_sidebar
from ui.upload import render_upload


def init_session_state() -> None:
    """Create the session_state keys the app uses, if they don't exist yet."""
    st.session_state.setdefault("uploader_key", 0)
    st.session_state.setdefault("file_name", None)
    st.session_state.setdefault("file_size", None)
    st.session_state.setdefault("file_bytes", None)
    st.session_state.setdefault("file_signature", None)
    st.session_state.setdefault("analysis", None)
    st.session_state.setdefault("chat_history", [])


def main() -> None:
    """Set up the page, sidebar and tabs."""
    st.set_page_config(page_title="Korpse - Legal Document Helper", layout="wide")
    init_session_state()
    render_sidebar()

    if USE_STUB:
        st.caption("🛠️ Development mode - showing sample data")

    upload_tab, review_tab, chat_tab, about_tab = st.tabs(
        ["Upload", "Review", "Ask a Question", "About and Privacy"]
    )
    with upload_tab:
        render_upload(backend)
    with review_tab:
        render_review()
    with chat_tab:
        render_chat(backend)
    with about_tab:
        render_about()


main()
