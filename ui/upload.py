"""Upload tab: choose a file, check it, and analyse it locally."""

import streamlit as st

from core.contract import (
    DocumentTooLargeError,
    EmptyDocumentError,
    ModelNotAvailableError,
    UnsupportedFileError,
)

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
        "The local AI model isn't set up yet. Please follow the setup steps in the README."
    ),
}
GENERIC_ERROR = "Something went wrong while analysing your document. Please try again."


def _check_file(name: str, size: int) -> str | None:
    """Return a friendly error message if the file is not acceptable, else None."""
    if not name.lower().endswith(ALLOWED_EXTENSIONS):
        return ERROR_MESSAGES[UnsupportedFileError]
    if size == 0:
        return "This file is empty. Please choose a file that contains text."
    if size > MAX_FILE_MB * 1024 * 1024:
        return f"This file is larger than {MAX_FILE_MB} MB. Please upload a smaller file."
    return None


def _analyse(backend, name: str, data: bytes) -> None:
    """Run the analysis and save the results in session_state."""
    try:
        with st.spinner("Reading your document locally..."):
            analysis = backend.analyze_document(data, name)
            # TODO: pass through safety/review.py review_analysis() once Ayush adds it.
    except tuple(ERROR_MESSAGES) as error:
        st.session_state["analysis"] = None
        st.error(ERROR_MESSAGES[type(error)])
        return
    except Exception:
        # Covers AnalysisError and anything unexpected. Never show the raw
        # error: it could contain document text.
        st.session_state["analysis"] = None
        st.error(GENERIC_ERROR)
        return

    st.session_state["file_name"] = name
    st.session_state["file_size"] = len(data)
    st.session_state["file_bytes"] = data
    st.session_state["analysis"] = analysis
    st.session_state["chat_history"] = []


def _show_file_info() -> None:
    """Show name, size and page count of the analysed document."""
    analysis = st.session_state["analysis"]
    size_kb = st.session_state["file_size"] / 1024
    st.success("Your document is ready. Open the **Review** tab to see the results.")
    name_col, size_col, pages_col = st.columns(3)
    name_col.metric("File", st.session_state["file_name"])
    size_col.metric("Size", f"{size_kb:,.1f} KB")
    pages_col.metric("Pages", analysis.page_count)


def render_upload(backend) -> None:
    """Draw the Upload tab."""
    st.header("Upload a document")
    st.write("Choose a rental agreement, contract or legal notice. It is processed on this device only.")

    uploaded = st.file_uploader(
        "Upload a legal document (PDF or .txt, up to 10 MB)",
        type=["pdf", "txt"],
        key=f"uploader_{st.session_state['uploader_key']}",
    )

    if uploaded is not None:
        problem = _check_file(uploaded.name, uploaded.size)
        if problem:
            st.error(problem)
            return

        # Only analyse a file once, not on every rerun of the page.
        signature = (uploaded.name, uploaded.size)
        if signature != st.session_state["file_signature"]:
            _analyse(backend, uploaded.name, uploaded.getvalue())
            if st.session_state["analysis"] is not None:
                st.session_state["file_signature"] = signature

    if st.session_state["analysis"] is not None:
        _show_file_info()
