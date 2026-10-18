
from pathlib import Path
from pypdf import PdfReader


def parse_document(file_path: str) -> dict:
    """Extract text from a local PDF or TXT file."""
    path = Path(file_path)

    if not path.is_file():
        return {
            "success": False,
            "error": "File not found."
        }

    suffix = path.suffix.lower()

    try:
        if suffix == ".txt":
            text = path.read_text(encoding="utf-8-sig")

            if not text.strip():
                return {
                    "success": False,
                    "error": "TXT file is empty."
                }

            return {
                "success": True,
                "file_name": path.name,
                "file_type": "txt",
                "pages": [{"page": None, "text": text}]
            }

        elif suffix == ".pdf":
            reader = PdfReader(str(path))

            if reader.is_encrypted:
                return {
                    "success": False,
                    "error": "Password-protected PDFs are not supported."
                }

            pages = []

            for page_number, page in enumerate(reader.pages, start=1):
                text = page.extract_text() or ""
                pages.append({
                    "page": page_number,
                    "text": text
                })

            if not any(p["text"].strip() for p in pages):
                return {
                    "success": False,
                    "error": "No extractable text found. The PDF may be scanned."
                }

            return {
                "success": True,
                "file_name": path.name,
                "file_type": "pdf",
                "pages": pages
            }

        return {
            "success": False,
            "error": "Unsupported file type. Use PDF or TXT."
        }

    except Exception:
        return {
            "success": False,
            "error": "Could not read the file. Check that it is valid and readable."
        }
