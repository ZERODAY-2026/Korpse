
from pprint import pprint

from ai.pipeline import analyze_document


sample_document = """
NOTICE TO VACATE

Date: 15 October 2026

To: Tenant

The landlord requests that the tenant vacate the rental property
by 25 October 2026 due to alleged non-payment of rent.

This notice is provided as a sample for testing only.
"""


if __name__ == "__main__":
    try:
        result = analyze_document(
            document_text=sample_document,
            jurisdiction="Unspecified",
        )
        pprint(result, sort_dicts=False)

    except (RuntimeError, ValueError) as error:
        print(f"Pipeline error: {error}")
