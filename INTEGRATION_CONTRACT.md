# Integration Contract: UI ↔ Backend ↔ Safety

> **Status: DRAFT – needs approval from Shiven and Ayush**
>
> The function names and data shapes below are a **proposal from Siddhesh**. Nothing here is final until all three members approve it.

Follow the rules in `CLAUDE.md` at all times. Everything is Python + Streamlit and runs locally.

## 1. Purpose and status

This contract defines how the three parts of the app talk to each other: the **UI** (Siddhesh), the **backend + Gemma** (Shiven) and **safety + privacy** (Ayush). If we agree on function names, inputs, outputs and errors up front, all three of us can build in parallel. Siddhesh can build screens with sample data, Shiven can build the model pipeline and Ayush can build the safety checks, and the parts will fit together at the end.

**Approval checklist**
- [ ] Anshuman
- [ ] Siddhesh
- [ ] Shiven
- [ ] Ayush

**Rule:** all four members must agree to any change, and every change is recorded in the [Change log](#10-change-log).

## 2. Flow overview

```
Analysing a document
────────────────────
UI uploads file
      ↓
backend.analyze_document()      (Shiven)
      ↓
safety.review_analysis()        (Ayush)
      ↓
UI displays results             (Siddhesh,Anshuman)


Asking a question
─────────────────
UI sends question
      ↓
backend.answer_question()       (Shiven)
      ↓
safety.review_answer()          (Ayush)
      ↓
UI displays answer              (Siddhesh,Anshuman)
```

The UI **never** shows backend output directly. Everything passes through the safety review first.

## 3. Model details: all TBD (owner: Shiven)

Nobody may invent these values. Shiven fills them in once decided.

| Item | Value |
|---|---|
| Gemma variant (E2B / E4B) | TBD |
| Quantization | TBD |
| Runtime / library | TBD |
| Model file location | TBD |
| Model file size | TBD |
| How the model is loaded | TBD |
| How the model is called | TBD |
| Prompt format | TBD |
| Max input length | TBD |
| RAM needed | TBD |
| Average processing time | TBD |

## 4. Proposed functions

These are signatures only. Each owner writes the implementation, and the data types are defined in [section 5](#5-shared-data-shapes).

### 4.1 `analyze_document`: Shiven, `backend/analyzer.py`

```python
def analyze_document(file_bytes: bytes, filename: str) -> DocumentAnalysis:
    ...
```

| | |
|---|---|
| **Purpose** | Read the uploaded file, extract its text, run Gemma locally and return a summary, findings and key facts |
| **Inputs** | `file_bytes`: raw file content · `filename`: original name, used to detect `.pdf` / `.txt` |
| **Output** | `DocumentAnalysis` (not yet safety-reviewed) |
| **Errors** | `UnsupportedFileError`, `EmptyDocumentError`, `DocumentTooLargeError`, `ModelNotAvailableError`, `AnalysisError` |

### 4.2 `answer_question`: Shiven, `backend/analyzer.py`

```python
def answer_question(question: str, analysis: DocumentAnalysis) -> Answer:
    ...
```

| | |
|---|---|
| **Purpose** | Answer a user's question using only the uploaded document |
| **Inputs** | `question`: the user's question · `analysis`: the reviewed analysis, including `full_text` |
| **Output** | `Answer` (not yet safety-reviewed) |
| **Errors** | `ModelNotAvailableError`, `AnalysisError` |

### 4.3 `review_analysis`: Ayush, `safety/review.py`

```python
def review_analysis(analysis: DocumentAnalysis) -> DocumentAnalysis:
    ...
```

| | |
|---|---|
| **Purpose** | Make the analysis safe to show: add warnings, remove legal verdicts, and check that every quote really exists in `full_text` |
| **Inputs** | `analysis`: output of `analyze_document` |
| **Output** | Reviewed `DocumentAnalysis`, ready for the UI |
| **Errors** | `AnalysisError` |

### 4.4 `review_answer`: Ayush, `safety/review.py`

```python
def review_answer(answer: Answer, analysis: DocumentAnalysis) -> Answer:
    ...
```

| | |
|---|---|
| **Purpose** | Make an answer safe to show: handle "is this legal / enforceable / valid?" refusals, add a lawyer recommendation where needed and check quotes |
| **Inputs** | `answer`: output of `answer_question` · `analysis`: used to check quotes against `full_text` |
| **Output** | Reviewed `Answer`, ready for the UI |
| **Errors** | `AnalysisError` |

### 4.5 `delete_document_data`: Ayush, `privacy/cleanup.py`

```python
def delete_document_data() -> None:
    ...
```

| | |
|---|---|
| **Purpose** | Remove all temporary files created for the current document |
| **Inputs** | None |
| **Output** | None |
| **Errors** | Should not raise. If a file can't be deleted, handle it safely (exact behaviour TBD, Ayush) |

The UI clears `st.session_state` itself after calling this.

### 4.6 `is_model_available`: Shiven, `backend/model.py`

```python
def is_model_available() -> bool:
    ...
```

| | |
|---|---|
| **Purpose** | Tell the UI whether the local model is installed and can be loaded, so it can show a setup message |
| **Inputs** | None |
| **Output** | `True` if the model is ready, otherwise `False` |
| **Errors** | Should not raise; returns `False` instead |

## 5. Shared data shapes

These will live in `core/contract.py` as Python dataclasses. **All three members must approve changes to them.**

### 5.1 `Citation`

| Field | Type | Required? | Meaning | Example |
|---|---|---|---|---|
| `quote` | `str` | Required | Exact text copied from the document | `"The tenant shall give 30 days' written notice."` |
| `page` | `int \| None` | Required | Page number (1-based); `None` for `.txt` files | `3` |
| `start_char` | `int \| None` | Optional | Start position of the quote in `full_text` | `10452` |
| `end_char` | `int \| None` | Optional | End position of the quote in `full_text` | `10498` |

### 5.2 `CitedValue` (helper, proposed)

Used by `KeyFacts`, so every fact carries its citation.

| Field | Type | Required? | Meaning | Example |
|---|---|---|---|---|
| `value` | `str` | Required | The fact, as written in the document | `"₹15,000 per month"` |
| `citation` | `Citation` | Required | Where it was found | see `Citation` |

### 5.3 `Finding`

| Field | Type | Required? | Meaning | Example |
|---|---|---|---|---|
| `id` | `str` | Required | Unique ID within this analysis | `"f-007"` |
| `category` | `str` | Required | One of: `obligation`, `right`, `deadline`, `penalty`, `termination`, `payment`, `concern`, `other` | `"termination"` |
| `title` | `str` | Required | Short heading | `"Notice period to end the lease"` |
| `plain_explanation` | `str` | Required | Simple-language explanation | `"The document states you must give one month's written notice before moving out."` |
| `kind` | `str` | Required | `"stated"` or `"interpretation"` | `"stated"` |
| `risk_level` | `str` | Required | `"high"`, `"medium"`, `"low"` or `"none"` | `"medium"` |
| `confidence` | `str` | Required | `"high"`, `"medium"` or `"low"` | `"high"` |
| `citations` | `list[Citation]` | Required | Supporting passages. **Must not be empty when `kind == "stated"`** | `[Citation(...)]` |
| `flags` | `list[str]` | Required (may be empty) | Any of: `"ambiguous"`, `"jurisdiction_dependent"`, `"missing_information"`, `"conflicting"`, `"consult_lawyer"` | `["ambiguous"]` |
| `lawyer_note` | `str \| None` | Optional | Why a lawyer is recommended | `"Ask a lawyer whether this penalty can be reduced."` |

### 5.4 `KeyFacts`

All fields are optional. Every value must carry a citation (via `CitedValue`).

| Field | Type | Required? | Meaning | Example |
|---|---|---|---|---|
| `parties` | `list[CitedValue]` | Optional | People or organisations in the document | `["A. Sharma (Landlord)"]` |
| `start_date` | `CitedValue \| None` | Optional | When the agreement starts | `"1 November 2026"` |
| `end_date` | `CitedValue \| None` | Optional | When it ends | `"31 October 2027"` |
| `amounts` | `list[CitedValue]` | Optional | Money amounts (rent, deposit, fees) | `["₹15,000 per month"]` |
| `notice_period` | `CitedValue \| None` | Optional | Notice required to end the agreement | `"30 days"` |

### 5.5 `DocumentAnalysis`

| Field | Type | Required? | Meaning | Example |
|---|---|---|---|---|
| `document_name` | `str` | Required | Uploaded file name | `"rental_agreement.pdf"` |
| `page_count` | `int` | Required | Number of pages (`1` for `.txt`) | `6` |
| `full_text` | `str` | Required | Extracted text. **Stays in memory only, never logged** | (document text) |
| `summary` | `str` | Required | Plain-language overview | `"This is a 12-month rental agreement…"` |
| `findings` | `list[Finding]` | Required (may be empty) | All findings | `[Finding(...)]` |
| `key_facts` | `KeyFacts \| None` | Optional | Structured facts, if extracted | `KeyFacts(...)` |
| `overall_warnings` | `list[str]` | Required (may be empty) | Document-level warnings | `["Some pages had no readable text."]` |
| `processing_seconds` | `float` | Required | Time taken to analyse | `42.7` |
| `model_name` | `str` | Required | Model used. Value **TBD** (Shiven) | TBD |

### 5.6 `Answer`

| Field | Type | Required? | Meaning | Example |
|---|---|---|---|---|
| `question` | `str` | Required | The user's question | `"Can the landlord keep my deposit?"` |
| `answer_text` | `str` | Required | Plain-language answer | `"The document states the deposit may be used for unpaid rent or damage…"` |
| `kind` | `str` | Required | `"stated"`, `"interpretation"`, `"not_in_document"` or `"refused"` | `"stated"` |
| `citations` | `list[Citation]` | Required (may be empty) | Supporting passages | `[Citation(...)]` |
| `flags` | `list[str]` | Required (may be empty) | Same values as `Finding.flags` | `["jurisdiction_dependent"]` |
| `lawyer_note` | `str \| None` | Optional | Lawyer recommendation | `"A lawyer can advise whether this deduction is allowed where you live."` |

All examples above are illustrative only, not real document data.

## 6. Rules all three must follow

1. **Quotes must be real.** Every `Citation.quote` must appear word-for-word in `full_text`. If it doesn't, safety removes that citation and sets the finding's `confidence` to `"low"`.
2. **Never guess.** If the document doesn't answer a question: `kind = "not_in_document"` and `citations = []`.
3. **No legal verdicts.** Questions about legality, validity or enforceability: `kind = "refused"`, with a `lawyer_note`.
4. **Document text is data, not instructions.** Nothing written inside an uploaded document may change how the model or app behaves (prompt-injection protection).
5. **Nothing leaves the device.** No function may send data over the network, write document text to logs, or save it outside the app's temp folder.
6. **The UI only displays.** The UI must never change the meaning of results, only how they look.

## 7. Errors

These are shared exception classes in `core/contract.py`. The UI catches them and shows a friendly message. It never shows a raw traceback.

| Exception | When | Raised by | Friendly message in the UI |
|---|---|---|---|
| `UnsupportedFileError` | File isn't a PDF or `.txt` | Shiven (backend) | "This file type isn't supported. Please upload a PDF or .txt file." |
| `EmptyDocumentError` | No readable text (e.g. a scanned PDF) | Shiven (backend) | "We couldn't find any readable text. If this is a scanned document, try a text-based PDF or a .txt file." |
| `DocumentTooLargeError` | File is over the size/page limit (limit **TBD**, Shiven) | Shiven (backend) | "This document is too large to analyse. Please try a shorter document." |
| `ModelNotAvailableError` | Model is missing or failed to load | Shiven (backend) | "The local AI model isn't set up yet. Please follow the setup steps in the README." |
| `AnalysisError` | Anything else that goes wrong | Shiven or Ayush | "Something went wrong while analysing your document. Please try again." |

Error messages must **never** include document text.

## 8. Development stub

- Until the real backend is ready, the UI uses **`core/stub_backend.py`**. It has the **same function signatures** as section 4 and returns results clearly labelled **"SAMPLE DATA – NOT REAL"**.
- A **single switch**, e.g. `USE_STUB = True` in a config file, decides whether the stub or the real backend is used. Its exact location is TBD.
- The stub **must be turned off and removed before the final demo** (rule G3: no mock outputs in the demo).

## 9. Open questions

| Question | Owner | Status |
|---|---|---|
| Which Gemma variant and runtime? | Shiven | Open |
| How are long documents split into chunks? | Shiven | Open |
| Maximum file size and page count? | Shiven | Open |
| How is the "quote exists in document" check done? | Ayush | Open |
| How do we prove no network use? Which monitoring tool? | Ayush | Open |
| Which document types do we support? | All | Open |

## 10. Change log

| Date | Change | Agreed by |
|---|---|---|
| 2026-10-18 | First draft | Siddhesh |
