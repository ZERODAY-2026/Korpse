# DRAFT - must be approved by Siddhesh, Shiven and Ayush before changes.
"""Shared data shapes and errors for the UI, backend and safety code.

Matches INTEGRATION_CONTRACT.md sections 5 (data shapes) and 7 (errors).
This file holds data definitions only: no model code and no network code.
"""

from dataclasses import dataclass, field
from typing import Literal

# Allowed values for the text fields below (see INTEGRATION_CONTRACT.md 5.3 and 5.6).
Category = Literal[
    "obligation", "right", "deadline", "penalty",
    "termination", "payment", "concern", "other",
]
FindingKind = Literal["stated", "interpretation"]
AnswerKind = Literal["stated", "interpretation", "not_in_document", "refused"]
RiskLevel = Literal["high", "medium", "low", "none"]
Confidence = Literal["high", "medium", "low"]
Flag = Literal[
    "ambiguous", "jurisdiction_dependent", "missing_information",
    "conflicting", "consult_lawyer",
]


# ---------------------------------------------------------------------------
# Data shapes
# ---------------------------------------------------------------------------

@dataclass(kw_only=True)
class Citation:
    """An exact passage copied from the document."""

    quote: str                      # must appear word-for-word in full_text
    page: int | None                # 1-based page number; None for .txt files
    start_char: int | None = None   # start position of the quote in full_text
    end_char: int | None = None     # end position of the quote in full_text


@dataclass(kw_only=True)
class CitedValue:
    """A single key fact together with where it was found (proposed helper)."""

    value: str
    citation: Citation


@dataclass(kw_only=True)
class Finding:
    """One obligation, right, deadline, risk, etc. found in the document."""

    id: str
    category: Category
    title: str
    plain_explanation: str
    kind: FindingKind
    risk_level: RiskLevel
    confidence: Confidence
    citations: list[Citation]       # must not be empty when kind == "stated"
    flags: list[Flag] = field(default_factory=list)
    lawyer_note: str | None = None


@dataclass(kw_only=True)
class KeyFacts:
    """Structured facts. Every field is optional and every value is cited."""

    parties: list[CitedValue] = field(default_factory=list)
    start_date: CitedValue | None = None
    end_date: CitedValue | None = None
    amounts: list[CitedValue] = field(default_factory=list)
    notice_period: CitedValue | None = None


@dataclass(kw_only=True)
class DocumentAnalysis:
    """Full result of analysing one document."""

    document_name: str
    page_count: int
    # Stays in memory only and is never logged; repr=False keeps it out of
    # printed or logged objects by accident.
    full_text: str = field(repr=False)
    summary: str
    findings: list[Finding] = field(default_factory=list)
    key_facts: KeyFacts | None = None
    overall_warnings: list[str] = field(default_factory=list)
    processing_seconds: float
    model_name: str                 # actual value TBD (Shiven)


@dataclass(kw_only=True)
class Answer:
    """Answer to one user question about the document."""

    question: str
    answer_text: str
    kind: AnswerKind
    citations: list[Citation] = field(default_factory=list)
    flags: list[Flag] = field(default_factory=list)
    lawyer_note: str | None = None


# ---------------------------------------------------------------------------
# Errors (INTEGRATION_CONTRACT.md section 7)
# Error messages must never include document text.
# ---------------------------------------------------------------------------

class UnsupportedFileError(Exception):
    """The file is not a PDF or .txt file. Raised by the backend."""


class EmptyDocumentError(Exception):
    """No readable text was found (e.g. a scanned PDF). Raised by the backend."""


class DocumentTooLargeError(Exception):
    """The file is over the size/page limit (limit TBD, Shiven). Raised by the backend."""


class ModelNotAvailableError(Exception):
    """The local model is missing or failed to load. Raised by the backend."""


class AnalysisError(Exception):
    """Anything else that goes wrong. Raised by the backend or safety code."""
