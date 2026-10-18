from pathlib import Path


# Application-level safety limits.
# These are our chosen limits, not limits specified by the hackathon guide.
MAX_FILE_SIZE_MB = 25
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
MAX_PAGES = 100

ALLOWED_EXTENSIONS = {".pdf", ".txt"}


def validate_file(file_path):
    """
    Validate a document before it enters the parsing/AI pipeline.
    """

    path = Path(file_path)

    # File must exist
    if not path.exists():
        return {
            "success": False,
            "message": "File does not exist."
        }

    # Path must point to a file
    if not path.is_file():
        return {
            "success": False,
            "message": "Provided path is not a file."
        }

    # Only PDF and TXT are accepted
    if path.suffix.lower() not in ALLOWED_EXTENSIONS:
        return {
            "success": False,
            "message": (
                f"Unsupported file type: {path.suffix}. "
                "Only PDF and TXT files are allowed."
            )
        }

    # File-size protection
    file_size = path.stat().st_size

    if file_size > MAX_FILE_SIZE_BYTES:
        return {
            "success": False,
            "message": (
                f"File is too large. Maximum allowed size is "
                f"{MAX_FILE_SIZE_MB} MB."
            )
        }

    # Empty-file protection
    if file_size == 0:
        return {
            "success": False,
            "message": "The uploaded file is empty."
        }

    return {
        "success": True,
        "message": "File passed safety validation.",
        "file_path": str(path)
    }


def validate_page_count(parsed_document):
    """
    Validate the number of pages extracted by the parser.

    TXT files do not require a page-count check.
    """

    if not isinstance(parsed_document, dict):
        return {
            "success": False,
            "message": "Invalid parser output."
        }

    pages = parsed_document.get("pages")

    if pages is None:
        return {
            "success": True,
            "message": "Page-count check not required."
        }

    if len(pages) > MAX_PAGES:
        return {
            "success": False,
            "message": (
                f"Document contains {len(pages)} pages. "
                f"The maximum allowed is {MAX_PAGES} pages."
            )
        }

    return {
        "success": True,
        "message": (
            f"Page count is within the allowed limit "
            f"({len(pages)} pages)."
        )
    }