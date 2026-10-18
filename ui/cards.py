"""Small display helpers shared by the UI tabs."""

import re

import streamlit as st

# Answer kinds: (text, icon, colour). Different icon and colour for each.
KIND_STYLES = {
    "stated": ("Stated in document", ":material/description:", "blue"),
    "interpretation": ("Possible interpretation", ":material/lightbulb:", "violet"),
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


def kind_badge(kind: str) -> None:
    """Show a small 'Stated in document' or 'Possible interpretation' badge."""
    if kind in KIND_STYLES:
        label, icon, color = KIND_STYLES[kind]
        st.badge(label, icon=icon, color=color)


def render_citations(citations) -> None:
    """Show each quote with its page number."""
    for citation in citations:
        page = f"Page {citation.page}" if citation.page is not None else "Text file (no page numbers)"
        st.caption(f":material/bookmark: {page}")
        quote = " ".join(citation.quote.split())  # keep the quote on one line
        st.markdown(f"> {safe(quote)}")


def render_flags(flags) -> None:
    """Show warning flags as short plain-language lines."""
    for flag in flags:
        st.markdown(f":orange[:material/flag:] {FLAG_TEXT.get(flag, safe(flag))}")
