"""Sidebar: disclaimer, privacy controls and how-it-works steps."""

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
        st.warning(
            "For advice about your situation, contact a qualified lawyer.",
            title="This is not legal advice",
            icon=":material/gavel:",
        )

        st.divider()
        st.subheader("Privacy", icon=":material/shield_lock:")
        st.success("Processed locally - nothing leaves this device", icon=":material/lock:")

        has_document = st.session_state.get("analysis") is not None
        st.button(
            "Delete document",
            icon=":material/delete:",
            on_click=_delete_document,
            disabled=not has_document,
            help="Removes the document and all results from this session.",
            width="stretch",
        )
        if st.session_state.pop("just_deleted", False):
            st.info("Document and results deleted.", icon=":material/check:")

        st.divider()
        st.subheader("How it works", icon=":material/help:")
        st.markdown(
            "1. :material/upload_file: **Upload** a PDF or .txt file.\n"
            "2. :material/fact_check: **Review** the summary and findings next to your document.\n"
            "3. :material/chat: **Ask a question** about the document."
        )
