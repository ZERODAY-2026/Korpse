
from document_parser import parse_document
from triage import build_triage_input

result = parse_document("samples/realcontract.pdf")

if not result["success"]:
    print("Parsing failed:", result["error"])
else:
    print("File:", result["file_name"])
    print("Pages extracted:", len(result["pages"]))

    for page in result["pages"][:2]:
        print(f"\n--- Page {page['page']} ---")
        print(page["text"][:500])

    triage = build_triage_input(result)

    if triage["success"]:
        print("\nChunks:", len(triage["chunks"]))
        print("Evidence passages:", len(triage["evidence_passages"]))
        print("Prompt prepared:", bool(triage["prompt"]))
