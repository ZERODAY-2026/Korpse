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

def test_pdf():
    result = parse_document("samples/samples.pdf")

    assert result["success"] is True, result
    assert result["file_type"] == "pdf"
    assert len(result["pages"]) >= 1
    assert "Party A" in result["pages"][0]["text"]
    assert result["pages"][0]["page"] == 1

    print("PASS: PDF parsing")


def test_empty_txt():
    result = parse_document("samples/empty.txt")
    assert result["success"] is False, result
    assert result["error"] == "TXT file is empty."
    print("PASS: Empty TXT handling")


def test_empty_or_image_only_pdf():
    # An empty PDF can be created in Word or another PDF tool.
    # This test uses the existing sample PDF only if it has no extractable text.
    result = parse_document("samples/empty.pdf")
    assert result["success"] is False, result
    assert "No extractable text found" in result["error"]
    print("PASS: Text-free PDF handling")



if __name__ == "__main__":
    test_txt()
    test_pdf()
    test_empty_txt()
    test_empty_or_image_only_pdf()
    test_missing_file()
    test_unsupported_file()
    print("All tests passed!")