"""Sidebar: disclaimer, privacy status, delete button and how-to steps."""

import streamlit as st


def _delete_document() -> None:
    """Clear everything about the current document from session_state."""
    # TODO: also call privacy/cleanup.py delete_document_data() once Ayush adds it.
    # A new uploader key makes Streamlit forget the file in the upload widget.
    next_uploader_key = st.session_state.get("uploader_key", 0) + 1
    st.session_state.clear()
    st.session_state["uploader_key"] = next_uploader_key
    st.session_state["just_deleted"] = True


def render_sidebar() -> None:
    """Draw the sidebar shown on every screen."""
    with st.sidebar:
        st.title("⚖️ Korpse")
        st.caption("Legal Document Helper")

        st.warning("**This is not legal advice.** For advice about your situation, contact a qualified lawyer.")
        st.success("🔒 Processed locally - nothing leaves this device")

        has_document = st.session_state.get("analysis") is not None
        st.button(
            "Delete document",
            icon="🗑️",
            on_click=_delete_document,
            disabled=not has_document,
            help="Removes the document and all results from this session.",
        )
        if st.session_state.pop("just_deleted", False):
            st.info("Document and results deleted.")

        st.subheader("How to use")
        st.markdown(
            "1. **Upload** a PDF or .txt file.\n"
            "2. **Review** the summary and findings next to your document.\n"
            "3. **Ask a question** about the document."
        )
