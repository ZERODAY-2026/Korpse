"""Minimal custom CSS. No external fonts, CDNs or internet images."""

import streamlit as st

# Text colours come from the active Streamlit theme. The few colours set here
# are mid-tone or semi-transparent so they stay visible in light and dark mode.
# Selectors use our own st.container keys (st-key-...), not Streamlit internals.
_CSS = """
<style>
/* File details on the Upload tab: smaller values than a normal metric. */
.st-key-file_info [data-testid="stMetricValue"] {
    font-size: 1.25rem;
}

/* Document panel: soft background, comfortable padding and line height. */
.st-key-doc_panel {
    background: rgba(128, 128, 128, 0.07);
    padding: 1rem 1.25rem;
}
.st-key-doc_panel [data-testid="stText"] {
    line-height: 1.75;
    font-size: 0.95rem;
}

.st-key-app_header {
    margin-top: -2rem;       /* move the header up, closer to the top bar */
}
.st-key-app_header h1 {
    font-size: 2.5rem;
    font-weight: 700;
    line-height: 1.2;
    letter-spacing: 0.04em;  /* a little air between letters */
    padding: 0;
}
/* Logo: the icon inside a soft rounded tile, about the height of the name.
   Streamlit renders an icon inside a heading as a span with role="img".
   Never write angle brackets in this CSS: st.html then drops the whole block. */
.st-key-app_header h1 span[role="img"] {
    font-size: 0.72em;
    padding: 0.28em;
    border-radius: 0.35em;
    background: rgba(28, 131, 225, 0.14);
    box-shadow: inset 0 0 0 1px rgba(28, 131, 225, 0.25);
    vertical-align: middle !important;  /* overrides Streamlit's inline style */
    margin-right: 0.2em;
    position: relative;
    top: -0.06em;
}
/* Tagline: small capitals with spacing. */
.st-key-app_header [data-testid="stCaptionContainer"] {
    font-size: 0.75rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}
</style>
"""


def apply_styles() -> None:
    """Add the app's small custom CSS to the page."""
    st.html(_CSS)
