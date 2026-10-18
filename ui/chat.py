"""Ask a Question tab: chat about the uploaded document."""

import streamlit as st

from core.contract import ModelNotAvailableError
from ui import backend_client
from ui.cards import kind_badge, render_citations, render_flags, safe


def _render_answer(answer) -> None:
    """Show one answer according to its kind."""
    if answer.kind == "not_in_document":
        st.info("The document does not mention this.", icon=":material/search_off:")
    elif answer.kind == "refused":
        message = safe(answer.answer_text)
        if answer.lawyer_note:
            message += "\n\n" + safe(answer.lawyer_note)
        st.warning(message, icon=":material/gavel:")
    else:
        kind_badge(answer.kind)
        st.markdown(safe(answer.answer_text))
        if answer.citations:
            render_citations(answer.citations)
        render_flags(answer.flags)
        if answer.lawyer_note:
            st.warning(safe(answer.lawyer_note), icon=":material/gavel:")


def _ask(question: str, analysis) -> None:
    """Get an answer and add it to the chat history."""
    try:
        with st.spinner("Looking for the answer in your document..."):
            answer = backend_client.answer_question(question, analysis)
            # TODO: pass through Ayush's safety review once it exists.
    except ModelNotAvailableError:
        st.error("The local AI model isn't available. Make sure Ollama is running.")
        return
    except Exception:
        # Never show the raw error: it could contain document text.
        st.error("Something went wrong while answering your question. Please try again.")
        return
    st.session_state["chat_history"].append(answer)


def render_chat() -> None:
    """Draw the Ask a Question tab."""
    analysis = st.session_state.get("analysis")
    if analysis is None:
        st.info("Upload a document first.")
        return

    st.header("Ask a question")
    if not backend_client.can_answer_questions():
        # The AI pipeline does not offer a question function yet.
        st.info(
            "Asking questions isn't available yet. The AI pipeline currently "
            "provides the document review only.",
            icon=":material/schedule:",
        )
        return
    st.caption("Answers come only from your document. They are not legal advice.")

    history = st.container()
    question = st.chat_input("Ask about your document")
    if question:
        _ask(question, analysis)

    with history:
        for answer in st.session_state["chat_history"]:
            with st.chat_message("user"):
                st.markdown(safe(answer.question))
            with st.chat_message("assistant"):
                _render_answer(answer)
