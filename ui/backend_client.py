"""The one place where the UI talks to the analysis backend.

USE_STUB = True  -> core/stub_backend.py (sample data, development only)
USE_STUB = False -> ai/pipeline.py from the feat/ai-pipeline branch (owner: Shiven)

Interface agreed with the AI pipeline (given by Siddhesh):
    analyze_file(file_path, jurisdiction="Unspecified") -> dict
with the keys document_type, summary, key_issues, important_dates, urgency,
urgency_reason, missing_information, disclaimer, file_name, file_type and
evidence_passages (list of {"page", "text", "categories"}).
"""

import re
import shutil
import tempfile
from pathlib import Path

from config import JURISDICTION, USE_STUB
from core.contract import (
    AnalysisError,
    EmptyDocumentError,
    ModelNotAvailableError,
    UnsupportedFileError,
)

URGENCY_LEVELS = ("high", "medium", "low", "unclear")
DEFAULT_DISCLAIMER = "This is general information, not legal advice."


def _load_backend():
    """Return the backend module chosen in config.py."""
    if USE_STUB:
        from core import stub_backend
        return stub_backend
    from ai import pipeline  # real AI pipeline (feat/ai-pipeline branch)
    return pipeline


def _safe_filename(name: str) -> str:
    """Keep only the base file name with safe characters (the extension matters)."""
    base = Path(name).name or "document"
    return re.sub(r"[^\w.\- ]", "_", base)


def analyze_upload(file_name: str, file_bytes: bytes) -> dict:
    """Analyse an uploaded file and return a checked result dictionary.

    The upload is written to a private temporary folder because
    analyze_file() needs a file path. The folder is deleted straight after.
    Raises the error classes from core/contract.py with no document text.
    """
    try:
        backend = _load_backend()
        analyze_file = backend.analyze_file
    except (ImportError, AttributeError) as error:
        raise ModelNotAvailableError("The AI pipeline is not connected.") from error

    folder = Path(tempfile.mkdtemp(prefix="korpse_"))
    try:
        path = folder / _safe_filename(file_name)
        path.write_bytes(file_bytes)
        result = analyze_file(str(path), jurisdiction=JURISDICTION)
    except (UnsupportedFileError, EmptyDocumentError, ModelNotAvailableError, AnalysisError):
        raise
    except ValueError as error:
        # ai/pipeline.py raises ValueError when the document text is empty.
        raise EmptyDocumentError("No readable text.") from error
    except RuntimeError as error:
        # ai/models.py raises RuntimeError("Cannot connect to Ollama...") when
        # the local model is not running. Only the type of problem is kept.
        if "ollama" in str(error).lower():
            raise ModelNotAvailableError("The local model is not running.") from error
        raise AnalysisError("The analysis failed.") from error
    except Exception as error:
        raise AnalysisError("The analysis failed.") from error
    finally:
        shutil.rmtree(folder, ignore_errors=True)

    return _check_result(result, file_name)


def can_answer_questions() -> bool:
    """True if the current backend supports questions about the document."""
    try:
        return hasattr(_load_backend(), "answer_question")
    except ImportError:
        return False


def answer_question(question: str, result: dict):
    """Ask the backend a question about the analysed document."""
    try:
        return _load_backend().answer_question(question, result)
    except (ImportError, AttributeError) as error:
        raise ModelNotAvailableError("Questions are not supported yet.") from error


# ---------------------------------------------------------------------------
# Checking the result before the UI uses it
# ---------------------------------------------------------------------------

def _text(value, default: str = "") -> str:
    """Return value if it is a string, else the default."""
    return value.strip() if isinstance(value, str) else default


def _text_list(value) -> list[str]:
    """Return only the non-empty strings from a list."""
    if not isinstance(value, list):
        return []
    return [item.strip() for item in value if isinstance(item, str) and item.strip()]


def _passages(value) -> list[dict]:
    """Return only well-formed evidence passages."""
    passages = []
    for item in value if isinstance(value, list) else []:
        if not isinstance(item, dict) or not _text(item.get("text")):
            continue
        page = item.get("page")
        passages.append({
            "page": page if isinstance(page, int) else None,
            "text": _text(item.get("text")),
            "categories": _text_list(item.get("categories")),
        })
    return passages


def _raise_for_failure(message: str) -> None:
    """Turn a {"success": False, "error": ...} result into a contract error."""
    lowered = message.lower()
    if "unsupported" in lowered:
        raise UnsupportedFileError("Unsupported file type.")
    if "empty" in lowered or "no extractable text" in lowered or "scanned" in lowered:
        raise EmptyDocumentError("No readable text.")
    raise AnalysisError("The document could not be read.")


def _check_result(result, file_name: str) -> dict:
    """Validate the backend's dictionary and fill safe defaults."""
    if not isinstance(result, dict):
        raise AnalysisError("The backend returned an unexpected result.")
    if result.get("success") is False:
        _raise_for_failure(_text(result.get("error")))

    urgency = _text(result.get("urgency")).lower()
    return {
        "document_type": _text(result.get("document_type"), "Unknown or unclear"),
        "summary": _text(result.get("summary")),
        "key_issues": _text_list(result.get("key_issues")),
        "important_dates": _text_list(result.get("important_dates")),
        "urgency": urgency if urgency in URGENCY_LEVELS else "unclear",
        "urgency_reason": _text(result.get("urgency_reason")),
        "missing_information": _text_list(result.get("missing_information")),
        "disclaimer": _text(result.get("disclaimer"), DEFAULT_DISCLAIMER),
        "file_name": _text(result.get("file_name"), file_name),
        "file_type": _text(result.get("file_type"), Path(file_name).suffix.lstrip(".")),
        "evidence_passages": _passages(result.get("evidence_passages")),
        # Not part of the pipeline output; the stub adds it. Shown in About.
        "model_name": _text(result.get("model_name")),
    }
