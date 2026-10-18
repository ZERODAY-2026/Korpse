"""Review tab: the document on the left, summary and findings on the right."""

import streamlit as st

from ui.cards import RISK_ORDER, render_finding, safe


def _render_document(analysis) -> None:
    """Show the full document text in a scrollable box."""
    st.subheader("Your document")
    st.caption(f"{analysis.document_name} · {analysis.page_count} page(s)")
    with st.container(height=600, border=True):
        # st.text shows plain text only, so nothing in the document is
        # treated as formatting, links or images.
        st.text(analysis.full_text)


def _render_results(analysis) -> None:
    """Show the summary, filters and finding cards."""
    st.subheader("Summary")
    st.markdown(safe(analysis.summary))
    for warning in analysis.overall_warnings:
        st.warning(safe(warning))

    st.subheader("Findings")
    findings = sorted(analysis.findings, key=lambda f: RISK_ORDER.get(f.risk_level, len(RISK_ORDER)))
    if not findings:
        st.info("No findings were identified in this document.")
        return

    risk_options = sorted({f.risk_level for f in findings}, key=lambda r: RISK_ORDER.get(r, len(RISK_ORDER)))
    category_options = sorted({f.category for f in findings})
    risk_col, category_col = st.columns(2)
    chosen_risks = risk_col.multiselect(
        "Risk level", risk_options, default=risk_options, format_func=str.capitalize
    )
    chosen_categories = category_col.multiselect(
        "Category", category_options, default=category_options, format_func=str.capitalize
    )

    shown = [f for f in findings if f.risk_level in chosen_risks and f.category in chosen_categories]
    if not shown:
        st.info("No findings match your filters.")
    for finding in shown:
        render_finding(finding)


def render_review() -> None:
    """Draw the Review tab as a split view."""
    analysis = st.session_state.get("analysis")
    if analysis is None:
        st.info("Upload a document first.")
        return

    left, right = st.columns([2, 3])
    with left:
        _render_document(analysis)
    with right:
        _render_results(analysis)
