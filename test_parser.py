

from document_parser import parse_document


def test_txt():
    result = parse_document("samples/sample.txt")
    assert result["success"] is True
    assert result["file_type"] == "txt"
    assert "Party A" in result["pages"][0]["text"]
    print("PASS: TXT parsing")


def test_missing_file():
    result = parse_document("samples/missing.txt")
    assert result["success"] is False
    assert "error" in result
    print("PASS: Missing-file handling")


def test_unsupported_file():
    result = parse_document("samples/document.docx")
    assert result["success"] is False
    print("PASS: Unsupported-file handling")


if __name__ == "__main__":
    test_txt()
    test_missing_file()
    test_unsupported_file()
    print("All tests passed!")

