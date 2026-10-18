"""Finding cards and small display helpers shared by the UI tabs."""

import re

import streamlit as st

# Risk badges: icon + coloured text label, never colour alone.
RISK_BADGES = {
    "high": "⛔ :red[**High risk**]",
    "medium": "⚠️ :orange[**Medium risk**]",
    "low": "ℹ️ :green[**Low risk**]",
    "none": "➖ :gray[**No risk noted**]",
}
RISK_ORDER = {"high": 0, "medium": 1, "low": 2, "none": 3}

KIND_LABELS = {
    "stated": "📄 **Stated in document**",
    "interpretation": "💭 *Possible interpretation*",
}

FLAG_TEXT = {
    "ambiguous": "The wording is unclear (ambiguous).",
    "jurisdiction_dependent": "This may depend on local law (jurisdiction).",
    "missing_information": "Some information is missing from the document.",
    "conflicting": "This may conflict with another part of the document.",
    "consult_lawyer": "Consider asking a qualified lawyer about this.",
}

_MARKDOWN_SPECIAL = re.compile(r"([\\`*_{}\[\]()#+\-.!|>~:$<])")


def safe(text: str) -> str:
    """Escape Markdown so document or model text is shown as plain text.

    This stops text inside a document from adding links, images (which could
    load from the internet) or formatting to the page.
    """
    return _MARKDOWN_SPECIAL.sub(r"\\\1", text)


def render_citations(citations) -> None:
    """Show each quote with its page number."""
    for citation in citations:
        page = f"Page {citation.page}" if citation.page is not None else "Text file (no page numbers)"
        st.caption(page)
        quote = " ".join(citation.quote.split())  # keep the quote on one line
        st.markdown(f"> {safe(quote)}")


def render_flags(flags) -> None:
    """Show warning flags as short plain-language lines."""
    for flag in flags:
        st.markdown(f"⚠️ {FLAG_TEXT.get(flag, safe(flag))}")


def render_finding(finding) -> None:
    """Draw one finding as a bordered card."""
    with st.container(border=True):
        st.markdown(
            f"{RISK_BADGES.get(finding.risk_level, safe(finding.risk_level))}"
            f" &nbsp;·&nbsp; {safe(finding.category.capitalize())}"
        )
        st.markdown(f"**{safe(finding.title)}**")
        st.markdown(safe(finding.plain_explanation))
        st.markdown(
            f"{KIND_LABELS.get(finding.kind, safe(finding.kind))}"
            f" &nbsp;·&nbsp; Confidence: {safe(finding.confidence.capitalize())}"
        )

        if finding.confidence == "low":
            st.warning("Low confidence: this result may be unreliable. Please check the source passage.")
        render_flags(finding.flags)
        if finding.lawyer_note:
            st.warning(safe(finding.lawyer_note))

        with st.expander("See source passage"):
            if finding.citations:
                render_citations(finding.citations)
            else:
                st.info("No source passage was found for this finding.")
