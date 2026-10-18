"""Upload tab: choose a file, check it, and analyse it locally."""

import streamlit as st

from core.contract import (
    DocumentTooLargeError,
    EmptyDocumentError,
    ModelNotAvailableError,
    UnsupportedFileError,
)
from ui import backend_client

MAX_FILE_MB = 10
ALLOWED_EXTENSIONS = (".pdf", ".txt")

# Friendly messages from INTEGRATION_CONTRACT.md section 7.
ERROR_MESSAGES = {
    UnsupportedFileError: "This file type isn't supported. Please upload a PDF or .txt file.",
    EmptyDocumentError: (
        "We couldn't find any readable text. If this is a scanned document, "
        "try a text-based PDF or a .txt file."
    ),
    DocumentTooLargeError: "This document is too large to analyse. Please try a shorter document.",
    ModelNotAvailableError: (
        "The local AI model isn't available. Make sure Ollama is running and "
        "follow the setup steps in the README."
    ),
}
GENERIC_ERROR = "Something went wrong while analysing your document. Please try again."

# Feature cards on the landing area: (icon, title, short text).
FEATURES = [
    (":material/summarize:", "Plain-language summary",
     "Key terms, risks and deadlines explained in everyday words."),
    (":material/format_quote:", "Cited sources",
     "Every finding shows the exact passage and page it comes from."),
    (":material/wifi_off:", "Private and offline",
     "Your document is processed on this device and never uploaded."),
]


def _check_file(name: str, size: int) -> str | None:
    """Return a friendly error message if the file is not acceptable, else None."""
    if not name.lower().endswith(ALLOWED_EXTENSIONS):
        return ERROR_MESSAGES[UnsupportedFileError]
    if size == 0:
        return "This file is empty. Please choose a file that contains text."
    if size > MAX_FILE_MB * 1024 * 1024:
        return f"This file is larger than {MAX_FILE_MB} MB. Please upload a smaller file."
    return None


def _analyse(name: str, data: bytes) -> None:
    """Run the analysis and save the results in session_state."""
    try:
        with st.spinner("Reading your document locally... this can take a minute or two."):
            analysis = backend_client.analyze_upload(name, data)
            # TODO: pass through Ayush's safety review once it exists.
    except tuple(ERROR_MESSAGES) as error:
        st.session_state["analysis"] = None
        st.error(ERROR_MESSAGES[type(error)], icon=":material/error:")
        return
    except Exception:
        # Covers AnalysisError and anything unexpected. Never show the raw
        # error: it could contain document text.
        st.session_state["analysis"] = None
        st.error(GENERIC_ERROR, icon=":material/error:")
        return

    st.session_state["file_name"] = name
    st.session_state["file_size"] = len(data)
    st.session_state["file_bytes"] = data
    st.session_state["analysis"] = analysis
    st.session_state["chat_history"] = []


def _show_file_info() -> None:
    """Show name, size and type of the analysed document."""
    analysis = st.session_state["analysis"]
    size_kb = st.session_state["file_size"] / 1024
    st.success(
        "Your document is ready. Open the **Review** tab to see the results.",
        icon=":material/check_circle:",
    )
    # The key adds a CSS class (st-key-file_info) for the smaller text in ui/styles.py.
    with st.container(key="file_info"):
        name_col, size_col, type_col = st.columns(3)
    name_col.metric("File", st.session_state["file_name"], icon=":material/draft:")
    size_col.metric("Size", f"{size_kb:,.1f} KB", icon=":material/straighten:")
    type_col.metric("Type", analysis["file_type"].upper() or "-", icon=":material/description:")


def _handle_upload() -> None:
    """Show the file uploader, check the file and analyse it once."""
    uploaded = st.file_uploader(
        "Upload a legal document (PDF or .txt, up to 10 MB)",
        type=["pdf", "txt"],
        key=f"uploader_{st.session_state['uploader_key']}",
    )
    if uploaded is None:
        return

    problem = _check_file(uploaded.name, uploaded.size)
    if problem:
        st.error(problem, icon=":material/error:")
        return

    # Only analyse a file once, not on every rerun of the page.
    signature = (uploaded.name, uploaded.size)
    if signature != st.session_state["file_signature"]:
        _analyse(uploaded.name, uploaded.getvalue())
        if st.session_state["analysis"] is not None:
            st.session_state["file_signature"] = signature


def _render_feature_cards() -> None:
    """Show three small cards explaining what the app does."""
    for column, (icon, title, text) in zip(st.columns(3), FEATURES):
        with column, st.container(border=True, height="stretch"):
            st.markdown(f"{icon} **{title}**")
            st.caption(text)


def render_upload() -> None:
    """Draw the Upload tab as a welcoming landing area."""
    st.header("Understand your legal document in simple language")
    st.caption(":material/lock: Runs privately on this device - your document never leaves your computer.")

    with st.container(border=True):
        _handle_upload()
        if st.session_state["analysis"] is not None:
            _show_file_info()

    st.space("small")
    _render_feature_cards()
