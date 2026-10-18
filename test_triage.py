print("test_triage.py started")
from document_parser import parse_document
from triage import (
    prepare_document,
    split_into_chunks,
    find_relevant_passages,
    build_triage_input,
)


def main():
    parsed = parse_document("samples/samples.pdf")
    assert parsed["success"], parsed

    prepared = prepare_document(parsed)
    assert prepared["success"], prepared
    assert prepared["full_text"].strip()

    chunks = split_into_chunks(prepared["full_text"], max_chars=500)
    assert chunks
    assert all(chunks)

    evidence = find_relevant_passages(prepared["pages"])
    print("PASS: Document preparation")
    print("PASS: Text chunking")
    print(f"PASS: Evidence detection ({len(evidence)} passages)")

    triage = build_triage_input(parsed)
    assert triage["success"]
    assert triage["prompt"]
    print("PASS: Triage prompt preparation")

    print("\nFirst detected passages:")
    for item in evidence[:5]:
        print(f"- Page {item['page']}: {item['text']}")

    print("\nAll triage tests passed!")


if __name__ == "__main__":
    main()
