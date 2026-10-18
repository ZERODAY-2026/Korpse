"""Ask a Question tab: chat about the uploaded document."""

import streamlit as st

from core.contract import ModelNotAvailableError
from ui.cards import KIND_LABELS, render_citations, render_flags, safe


def _render_answer(answer) -> None:
    """Show one answer according to its kind."""
    if answer.kind == "not_in_document":
        st.info("The document does not mention this.")
    elif answer.kind == "refused":
        message = safe(answer.answer_text)
        if answer.lawyer_note:
            message += "\n\n" + safe(answer.lawyer_note)
        st.warning(message)
    else:
        st.markdown(safe(answer.answer_text))
        st.markdown(KIND_LABELS.get(answer.kind, safe(answer.kind)))
        if answer.citations:
            render_citations(answer.citations)
        render_flags(answer.flags)
        if answer.lawyer_note:
            st.warning(safe(answer.lawyer_note))


def _ask(backend, question: str, analysis) -> None:
    """Get an answer and add it to the chat history."""
    try:
        with st.spinner("Looking for the answer in your document..."):
            answer = backend.answer_question(question, analysis)
            # TODO: pass through safety/review.py review_answer() once Ayush adds it.
    except ModelNotAvailableError:
        st.error("The local AI model isn't set up yet. Please follow the setup steps in the README.")
        return
    except Exception:
        # Never show the raw error: it could contain document text.
        st.error("Something went wrong while answering your question. Please try again.")
        return
    st.session_state["chat_history"].append(answer)


def render_chat(backend) -> None:
    """Draw the Ask a Question tab."""
    analysis = st.session_state.get("analysis")
    if analysis is None:
        st.info("Upload a document first.")
        return

    st.header("Ask a question")
    st.caption("Answers come only from your document. They are not legal advice.")

    history = st.container()
    question = st.chat_input("Ask about your document")
    if question:
        _ask(backend, question, analysis)

    with history:
        for answer in st.session_state["chat_history"]:
            with st.chat_message("user"):
                st.markdown(safe(answer.question))
            with st.chat_message("assistant"):
                _render_answer(answer)
