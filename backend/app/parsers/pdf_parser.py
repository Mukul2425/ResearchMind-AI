def parse_pdf(raw_bytes: bytes) -> dict:
    # Placeholder parser output. Swap in PyMuPDF/pdfplumber + section detection.
    return {
        "sections": [
            {"name": "Abstract", "text": ""},
            {"name": "Introduction", "text": ""},
        ],
        "size": len(raw_bytes),
    }
