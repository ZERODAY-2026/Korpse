from pathlib import Path

from safety import (
    MAX_FILE_SIZE_MB,
    MAX_PAGES,
    validate_file,
    validate_page_count,
)


def test_allowed_file():
    result = validate_file("samples/samples.pdf")

    assert result["success"] is True, result

    print("PASS: Valid PDF accepted")


def test_missing_file():
    result = validate_file("samples/does_not_exist.pdf")

    assert result["success"] is False

    print("PASS: Missing file rejected")


def test_unsupported_file():
    test_file = Path("samples/test.exe")

    try:
        test_file.write_text("fake executable")

        result = validate_file(test_file)

        assert result["success"] is False

        print("PASS: Unsupported file type rejected")

    finally:
        if test_file.exists():
            test_file.unlink()


def test_empty_file():
    test_file = Path("samples/empty_test.pdf")

    try:
        test_file.write_bytes(b"")

        result = validate_file(test_file)

        assert result["success"] is False

        print("PASS: Empty file rejected")

    finally:
        if test_file.exists():
            test_file.unlink()


def test_page_count():
    fake_document = {
        "pages": [1, 2, 3]
    }

    result = validate_page_count(fake_document)

    assert result["success"] is True, result

    print("PASS: Page count accepted")


def main():
    print("Running safety tests...")
    print(f"Maximum file size: {MAX_FILE_SIZE_MB} MB")
    print(f"Maximum pages: {MAX_PAGES}")
    print()

    test_allowed_file()
    test_missing_file()
    test_unsupported_file()
    test_empty_file()
    test_page_count()

    print()
    print("All safety tests passed!")


if __name__ == "__main__":
    main()