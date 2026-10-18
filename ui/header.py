"""App header: logo and name in the upper-left corner of the main area."""

import streamlit as st

APP_NAME = "KØRPSE"

# Logo icon and the Ø share Streamlit's theme-aware blue, so they match in
# light and dark mode. The tile around the icon is styled in ui/styles.py.
_LOGO = ":blue[:material/balance:]"
_WORDMARK = "K:blue[Ø]RPSE"


def render_header() -> None:
    """Show the logo and app name side by side, aligned left."""
    # The key gives the container a CSS class (st-key-app_header) used in ui/styles.py.
    with st.container(key="app_header"):
        st.title(f"{_LOGO} {_WORDMARK}", anchor=False)
        st.caption("Legal Document Helper")
