"""Review tab: cited passages on the left, the triage panel on the right."""

import streamlit as st

from ui.cards import safe

# Urgency: (text, icon, colour). Always shown together, never colour alone.
URGENCY_STYLES = {
    "high": ("High", ":material/error:", "red"),
    "medium": ("Medium", ":material/warning:", "orange"),
    "low": ("Low", ":material/info:", "green"),
    "unclear": ("Unclear", ":material/help:", "gray"),
}

# Readable names for the passage categories used by the AI pipeline (triage.py).
CATEGORY_NAMES = {
    "obligations": "Obligations",
    "deadlines": "Deadlines",
    "termination": "Termination",
    "penalties_and_payments": "Penalties and payments",
    "risks_and_ambiguities": "Risks and ambiguities",
}


def _render_list(items: list[str], empty_text: str) -> None:
    """Show a bullet list, or a short note when the list is empty."""
    if items:
        st.markdown("\n".join(f"- {safe(item)}" for item in items))
    else:
        st.caption(empty_text)


def _section(icon: str, title: str) -> None:
    """Show a small section heading with an icon."""
    st.markdown(f"{icon} **{title}**")


def _render_passages(result: dict) -> None:
    """Show the evidence passages (exact quotes with page numbers)."""
    passages = result["evidence_passages"]
    st.subheader("From your document", icon=":material/format_quote:")
    st.caption(f"{safe(result['file_name'])} · {len(passages)} cited passage(s)")

    # The key adds a CSS class (st-key-doc_panel) for the soft background in ui/styles.py.
    with st.container(height=600, border=True, key="doc_panel"):
        if not passages:
            st.caption("No supporting passages were found.")
        for passage in passages:
            page = f"Page {passage['page']}" if passage["page"] is not None else "Text file"
            categories = ", ".join(CATEGORY_NAMES.get(c, safe(c)) for c in passage["categories"])
            st.caption(f":material/bookmark: {page}" + (f" · {categories}" if categories else ""))
            # st.text shows plain text only, so nothing in the document is
            # treated as formatting, links or images.
            st.text(passage["text"])


def _render_triage(result: dict) -> None:
    """Show the triage result in a single panel."""
    with st.container(border=True, gap="medium"):
        st.subheader("LEGAL DOCUMENT TRIAGE", anchor=False, divider="gray", text_alignment="center")

        type_col, urgency_col = st.columns([3, 2], vertical_alignment="center")
        with type_col:
            _section(":material/description:", "Document type")
            st.markdown(safe(result["document_type"]))
        label, icon, color = URGENCY_STYLES[result["urgency"]]
        urgency_col.metric(f":{color}[Urgency]", label, icon=icon, border=True)
        if result["urgency_reason"]:
            st.caption(f"{icon} {safe(result['urgency_reason'])}")

        with st.container(gap="small"):
            _section(":material/summarize:", "Summary")
            st.markdown(safe(result["summary"]) if result["summary"] else "No summary was returned.")

        with st.container(gap="small"):
            _section(":material/warning:", "Key issues")
            _render_list(result["key_issues"], "No key issues were identified.")

        with st.container(gap="small"):
            _section(":material/event:", "Important dates")
            _render_list(result["important_dates"], "No dates or deadlines were found.")

        with st.container(gap="small"):
            _section(":material/help:", "Missing information")
            _render_list(result["missing_information"], "Nothing obviously missing was noted.")

        st.caption(f":material/gavel: {safe(result['disclaimer'])}")


def render_review() -> None:
    """Draw the Review tab as a split view."""
    result = st.session_state.get("analysis")
    if result is None:
        st.info("Upload a document first.")
        return

    left, right = st.columns([2, 3], gap="large")
    with left:
        _render_passages(result)
    with right:
        _render_triage(result)
