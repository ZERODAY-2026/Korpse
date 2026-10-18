"""Korpse - Private Legal Document Triage Agent (Streamlit entry point)."""

import streamlit as st

from config import USE_STUB
# The backend (stub or real AI pipeline) is chosen in ui/backend_client.py.
from ui.about import render_about
from ui.chat import render_chat
from ui.header import render_header
from ui.review import render_review
from ui.sidebar import render_sidebar
from ui.styles import apply_styles
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
    st.set_page_config(page_title="KØRPSE - Legal Document Helper", layout="wide")
    # Hide Streamlit's developer options (Deploy, Rerun, Clear cache) from the
    # toolbar and menu. Deploying to the cloud would break the on-device rule.
    st.set_option("client.toolbarMode", "viewer")
    init_session_state()
    apply_styles()
    render_sidebar()
    render_header()

    if USE_STUB:
        st.caption("🛠️ Development mode - showing sample data")

    upload_tab, review_tab, chat_tab, about_tab = st.tabs(
        ["Upload", "Review", "Ask a Question", "About and Privacy"]
    )
    with upload_tab:
        render_upload()
    with review_tab:
        render_review()
    with chat_tab:
        render_chat()
    with about_tab:
        render_about()


main()
