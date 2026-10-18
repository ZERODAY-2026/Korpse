# ###########################################################################
# #                                                                         #
# #   DEVELOPMENT ONLY - remove before final demo (rule G3)                 #
# #                                                                         #
# #   This file returns SAMPLE DATA - NOT REAL. It lets the UI be built     #
# #   before the real backend is ready. It does not use any AI model.       #
# #                                                                         #
# ###########################################################################
"""Fake backend with the same function names as the real one.

See INTEGRATION_CONTRACT.md section 8. No model code, no network code.
"""

import re
import time

from core.contract import (
    Answer,
    Citation,
    CitedValue,
    DocumentAnalysis,
    EmptyDocumentError,
    Finding,
    KeyFacts,
    UnsupportedFileError,
)

SAMPLE_LABEL = "SAMPLE DATA - NOT REAL"

# Made-up rental agreement used as full_text for PDF uploads.
# All names, places and amounts are fictional.
SAMPLE_PAGES = [
    (
        "RESIDENTIAL RENTAL AGREEMENT\n"
        "This Rental Agreement is made on 1 November 2026 between Ravi Kumar "
        "(the Landlord) and Priya Nair (the Tenant).\n"
        "1. Property. The Landlord agrees to rent Flat 4B, Green Park "
        "Apartments, Dharwad, to the Tenant for residential use only.\n"
        "2. Term. The tenancy starts on 1 November 2026 and ends on "
        "31 October 2027.\n"
        "3. Rent. The monthly rent is Rs. 15,000, payable on or before the "
        "5th day of each month."
    ),
    (
        "4. Late payment. If rent is not paid by the due date, the Tenant "
        "shall pay a late fee of Rs. 500 per day until the rent is paid in full.\n"
        "5. Security deposit. The Tenant shall pay a security deposit of "
        "Rs. 45,000. The Landlord may deduct any amount from the security "
        "deposit at the Landlord's sole discretion.\n"
        "6. Rent increase. The rent shall increase by 10% at the time of "
        "any renewal."
    ),
    (
        "7. Repairs. The Tenant shall be responsible for all minor repairs "
        "to the property.\n"
        "8. Termination. The Landlord may terminate this agreement by giving "
        "15 days' notice. The Tenant may terminate this agreement by giving "
        "two months' written notice.\n"
        "9. Signatures. Signed by the Landlord and the Tenant on the date "
        "first written above."
    ),
]
SAMPLE_TEXT = "\n\n".join(SAMPLE_PAGES)

# Fake findings: (fields, quote). Every quote is copied from SAMPLE_TEXT.
SAMPLE_FINDINGS = [
    (
        dict(
            id="f-001", category="penalty", title="Daily late fee on rent",
            plain_explanation=(
                "The document states a late fee of Rs. 500 for every day "
                "rent is late, with no upper limit. You may want to ask "
                "whether the fee can be capped."
            ),
            kind="stated", risk_level="high", confidence="high",
            flags=["jurisdiction_dependent"],
            lawyer_note="Limits on late fees can depend on local law. A lawyer can advise.",
        ),
        "a late fee of Rs. 500 per day until the rent is paid in full",
    ),
    (
        dict(
            id="f-002", category="termination", title="Unequal notice periods",
            plain_explanation=(
                "This may mean the landlord can end the agreement much faster "
                "than you can (15 days versus two months). You may want to "
                "ask for equal notice periods."
            ),
            kind="interpretation", risk_level="high", confidence="medium",
            flags=["consult_lawyer"],
            lawyer_note="Consider asking a qualified lawyer about the unequal notice terms.",
        ),
        "The Landlord may terminate this agreement by giving 15 days' notice.",
    ),
    (
        dict(
            id="f-003", category="concern", title="Deposit deductions at landlord's discretion",
            plain_explanation=(
                "The document states the landlord may deduct any amount from "
                "the deposit at their sole discretion (their own choice). It "
                "does not say what deductions are for. You may want to ask "
                "for a list of allowed deductions."
            ),
            kind="stated", risk_level="medium", confidence="high",
            flags=["ambiguous", "jurisdiction_dependent"],
        ),
        "The Landlord may deduct any amount from the security deposit at the Landlord's sole discretion.",
    ),
    (
        dict(
            id="f-004", category="obligation", title="'Minor repairs' is not defined",
            plain_explanation=(
                "This may mean you pay for repairs, but the document does not "
                "say what counts as 'minor'. You may want to ask for examples "
                "or a cost limit."
            ),
            kind="interpretation", risk_level="medium", confidence="low",
            flags=["ambiguous", "missing_information"],
        ),
        "The Tenant shall be responsible for all minor repairs to the property.",
    ),
    (
        dict(
            id="f-005", category="payment", title="10% rent increase on renewal",
            plain_explanation=(
                "The document states the rent goes up by 10% if the agreement "
                "is renewed. You may want to check this before renewing."
            ),
            kind="stated", risk_level="low", confidence="high",
        ),
        "The rent shall increase by 10% at the time of any renewal.",
    ),
    (
        dict(
            id="f-006", category="deadline", title="Rent due by the 5th",
            plain_explanation=(
                "The document states rent must be paid on or before the 5th "
                "of each month. You may want to set a reminder."
            ),
            kind="stated", risk_level="low", confidence="high",
        ),
        "payable on or before the 5th day of each month",
    ),
]

# Fake key facts: (field name, value, quote).
SAMPLE_KEY_FACTS = [
    ("parties", "Ravi Kumar (Landlord)", "Ravi Kumar (the Landlord)"),
    ("parties", "Priya Nair (Tenant)", "Priya Nair (the Tenant)"),
    ("start_date", "1 November 2026", "The tenancy starts on 1 November 2026"),
    ("end_date", "31 October 2027", "ends on 31 October 2027"),
    ("amounts", "Rs. 15,000 per month (rent)", "The monthly rent is Rs. 15,000"),
    ("amounts", "Rs. 45,000 (security deposit)", "a security deposit of Rs. 45,000"),
    ("notice_period", "Two months (tenant) / 15 days (landlord)",
     "The Tenant may terminate this agreement by giving two months' written notice."),
]

REFUSAL_WORDS = ("legal", "enforceable", "valid")
NOT_IN_DOCUMENT_PATTERN = re.compile(r"\bpets?\b", re.IGNORECASE)


# ---------------------------------------------------------------------------
# Public functions (same names as INTEGRATION_CONTRACT.md section 4)
# ---------------------------------------------------------------------------

def is_model_available() -> bool:
    """Pretend the model is always ready."""
    return True


def analyze_document(file_bytes: bytes, filename: str) -> DocumentAnalysis:
    """Return a fake analysis. .txt uses the real text; PDF uses SAMPLE_TEXT."""
    started = time.perf_counter()
    time.sleep(1)  # short pause so the UI spinner can be seen

    name = filename.lower()
    if name.endswith(".txt"):
        full_text = file_bytes.decode("utf-8", errors="replace")
        if not full_text.strip():
            raise EmptyDocumentError("The uploaded text file is empty.")
        pages = None
        page_count = 1
    elif name.endswith(".pdf"):
        full_text = SAMPLE_TEXT
        pages = SAMPLE_PAGES
        page_count = len(SAMPLE_PAGES)
    else:
        raise UnsupportedFileError("Only .pdf and .txt files are supported.")

    findings = _build_findings(full_text, pages)
    key_facts = _build_key_facts(full_text, pages)

    return DocumentAnalysis(
        document_name=filename,
        page_count=page_count,
        full_text=full_text,
        summary=(
            f"[{SAMPLE_LABEL}] This is a 12-month residential rental agreement "
            "between a landlord and a tenant. It sets the rent, a security "
            "deposit, late fees, repair duties and how either side can end the "
            "agreement. The biggest concerns are a daily late fee with no limit "
            "and unequal notice periods."
        ),
        findings=findings,
        key_facts=key_facts,
        overall_warnings=[f"{SAMPLE_LABEL}: these results come from the development stub."],
        processing_seconds=round(time.perf_counter() - started, 2),
        model_name=f"{SAMPLE_LABEL} (stub backend, no model)",
    )


def answer_question(question: str, analysis: DocumentAnalysis) -> Answer:
    """Return a fake answer: refused, not_in_document, or a normal cited answer."""
    lowered = question.lower()

    if any(word in lowered for word in REFUSAL_WORDS):
        return Answer(
            question=question,
            answer_text=(
                f"[{SAMPLE_LABEL}] I can't say whether this is legal, valid or "
                "enforceable. I can only explain what the document states."
            ),
            kind="refused",
            flags=["consult_lawyer"],
            lawyer_note="For a legal opinion, please consult a qualified lawyer.",
        )

    if NOT_IN_DOCUMENT_PATTERN.search(question):
        return Answer(
            question=question,
            answer_text=f"[{SAMPLE_LABEL}] The document does not mention this.",
            kind="not_in_document",
        )

    cited = next((f for f in analysis.findings if f.citations), None)
    return Answer(
        question=question,
        answer_text=(
            f"[{SAMPLE_LABEL}] The document states the following on this topic. "
            "See the cited passage below."
        ),
        kind="stated",
        citations=list(cited.citations) if cited else [],
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _cite(quote: str, full_text: str, pages: list[str] | None) -> Citation | None:
    """Build a Citation if the quote is found word-for-word, else None."""
    start = full_text.find(quote)
    if start == -1:
        return None
    return Citation(
        quote=quote,
        page=_page_for(start, pages),
        start_char=start,
        end_char=start + len(quote),
    )


def _page_for(position: int, pages: list[str] | None) -> int | None:
    """Return the 1-based page that contains a character position."""
    if pages is None:
        return None
    page_start = 0
    for number, page_text in enumerate(pages, start=1):
        page_end = page_start + len(page_text)
        if position < page_end:
            return number
        page_start = page_end + 2  # the "\n\n" between pages
    return len(pages)


def _sentences(text: str) -> list[str]:
    """Split text into non-empty sentences or lines."""
    parts = re.split(r"(?<=[.!?])\s+|\n+", text)
    return [part.strip() for part in parts if part.strip()]


def _build_findings(full_text: str, pages: list[str] | None) -> list[Finding]:
    """Create the fake findings with citations that exist in full_text.

    For an uploaded .txt the sample quotes usually are not in the text, so a
    real sentence from the upload is quoted instead. The explanation then does
    not match the quote; that is fine because it is all sample data.
    """
    sentences = _sentences(full_text)
    findings = []
    for index, (fields, quote) in enumerate(SAMPLE_FINDINGS):
        citation = _cite(quote, full_text, pages)
        if citation is None and sentences:
            citation = _cite(sentences[index % len(sentences)], full_text, pages)
        findings.append(Finding(citations=[citation] if citation else [], **fields))
    return findings


def _build_key_facts(full_text: str, pages: list[str] | None) -> KeyFacts | None:
    """Create fake key facts, keeping only those whose quote is in full_text."""
    facts = KeyFacts()
    for field_name, value, quote in SAMPLE_KEY_FACTS:
        citation = _cite(quote, full_text, pages)
        if citation is None:
            continue
        cited_value = CitedValue(value=value, citation=citation)
        if field_name in ("parties", "amounts"):
            getattr(facts, field_name).append(cited_value)
        else:
            setattr(facts, field_name, cited_value)

    if facts == KeyFacts():
        return None
    return facts
