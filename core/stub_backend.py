# ###########################################################################
# #                                                                         #
# #   DEVELOPMENT ONLY - remove before final demo (rule G3)                 #
# #                                                                         #
# #   This file returns SAMPLE DATA - NOT REAL. It lets the UI be built     #
# #   before the real backend is ready. It does not use any AI model.       #
# #                                                                         #
# ###########################################################################
"""Fake backend with the same analyze_file() interface as ai/pipeline.py.

Returns the same dictionary shape as the AI pipeline. No model code, no
network code.
"""

import re
import time
from pathlib import Path

from core.contract import Answer, Citation, EmptyDocumentError, UnsupportedFileError

SAMPLE_LABEL = "SAMPLE DATA - NOT REAL"

# Made-up rental agreement used for PDF uploads.
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

# Fake evidence passages: (page, quote, categories). Every quote is copied
# word-for-word from SAMPLE_PAGES. Categories use the names from triage.py.
SAMPLE_EVIDENCE = [
    (1, "The monthly rent is Rs. 15,000, payable on or before the 5th day of each month.",
     ["deadlines", "penalties_and_payments"]),
    (2, "If rent is not paid by the due date, the Tenant shall pay a late fee of Rs. 500 "
        "per day until the rent is paid in full.",
     ["obligations", "penalties_and_payments"]),
    (2, "The Landlord may deduct any amount from the security deposit at the Landlord's "
        "sole discretion.",
     ["risks_and_ambiguities"]),
    (3, "The Tenant shall be responsible for all minor repairs to the property.",
     ["obligations"]),
    (3, "The Landlord may terminate this agreement by giving 15 days' notice.",
     ["termination"]),
    (3, "The Tenant may terminate this agreement by giving two months' written notice.",
     ["termination", "deadlines"]),
]

SAMPLE_RESULT = {
    "document_type": "Residential Rental Agreement",
    "summary": (
        f"[{SAMPLE_LABEL}] This is a 12-month rental agreement between a landlord "
        "and a tenant. It sets the rent, a security deposit, late fees, repair "
        "duties and how either side can end the agreement."
    ),
    "key_issues": [
        "A late fee of Rs. 500 per day applies, with no upper limit stated.",
        "The landlord can end the agreement with 15 days' notice, but the tenant "
        "must give two months' notice.",
        "The landlord may deduct any amount from the deposit at their sole discretion.",
        "'Minor repairs' is not defined.",
    ],
    "important_dates": [
        "Tenancy starts on 1 November 2026 and ends on 31 October 2027.",
        "Rent is due on or before the 5th day of each month.",
        "Two months' written notice is needed for the tenant to end the agreement.",
    ],
    "urgency": "medium",
    "urgency_reason": "The late fee and unequal notice periods warrant review before signing.",
    "missing_information": [
        "The applicable jurisdiction is not specified.",
        "No limit on the total late fee is stated.",
    ],
    "disclaimer": "This is general information, not legal advice.",
}

REFUSAL_WORDS = ("legal", "enforceable", "valid")
NOT_IN_DOCUMENT_PATTERN = re.compile(r"\bpets?\b", re.IGNORECASE)


def is_model_available() -> bool:
    """Pretend the model is always ready."""
    return True


def analyze_file(file_path: str, jurisdiction: str = "Unspecified") -> dict:
    """Return a fake result in the same shape as ai/pipeline.py analyze_file()."""
    time.sleep(1)  # short pause so the UI spinner can be seen
    path = Path(file_path)
    suffix = path.suffix.lower()

    if suffix == ".pdf":
        passages = [
            {"page": page, "text": text, "categories": categories}
            for page, text, categories in SAMPLE_EVIDENCE
        ]
    elif suffix == ".txt":
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        if not text.strip():
            raise EmptyDocumentError("The uploaded text file is empty.")
        # Quote real sentences from the upload so every quote exists in it.
        passages = [
            {"page": None, "text": sentence, "categories": []}
            for sentence in _sentences(text)[:6]
        ]
    else:
        raise UnsupportedFileError("Only .pdf and .txt files are supported.")

    return {
        **SAMPLE_RESULT,
        "file_name": path.name,
        "file_type": suffix.lstrip("."),
        "evidence_passages": passages,
        "model_name": f"{SAMPLE_LABEL} (stub backend, no model)",
    }


def answer_question(question: str, result: dict) -> Answer:
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

    passages = result.get("evidence_passages") or []
    citations = [Citation(quote=passages[0]["text"], page=passages[0]["page"])] if passages else []
    return Answer(
        question=question,
        answer_text=(
            f"[{SAMPLE_LABEL}] The document states the following on this topic. "
            "See the cited passage below."
        ),
        kind="stated",
        citations=citations,
    )


def _sentences(text: str) -> list[str]:
    """Split text into non-empty sentences or lines."""
    parts = re.split(r"(?<=[.!?])\s+|\n+", text)
    return [part.strip() for part in parts if part.strip()]
