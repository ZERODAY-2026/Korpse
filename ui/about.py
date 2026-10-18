"""About and Privacy tab."""

import streamlit as st

from ui.cards import safe


def render_about() -> None:
    """Draw the About and Privacy tab."""
    analysis = st.session_state.get("analysis")
    if analysis is None:
        st.info("Upload a document first.")
        return

    st.header("About and Privacy")

    st.subheader("How it works")
    st.markdown(
        "- Your document is read and analysed **on this device only**.\n"
        "- A local AI model finds obligations, rights, deadlines, penalties and risks.\n"
        "- Every finding shows the exact passage and page it comes from.\n"
        "- Nothing is uploaded to the internet, and nothing is saved after you delete the document."
    )

    st.subheader("Model")
    st.markdown(f"Model used: **{safe(analysis.get('model_name') or 'Local AI model (details TBD)')}**")

    st.subheader("Limitations")
    st.markdown(
        "- The app can miss things or misunderstand wording.\n"
        "- Scanned (image-only) PDFs can't be read.\n"
        "- It does not know the law where you live.\n"
        "- It can't say whether something is legal, valid or enforceable."
    )

    st.subheader("Not legal advice")
    st.warning(
        "This tool provides general information only and is not legal advice. "
        "For advice about your situation, contact a qualified lawyer."
    )
