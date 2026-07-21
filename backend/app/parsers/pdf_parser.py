from collections import OrderedDict
import re

import fitz


CANONICAL_SECTIONS: list[tuple[str, str]] = [
    (r"^abstract$", "Abstract"),
    (r"^introduction$", "Introduction"),
    (r"^(related work|background)$", "Related Work"),
    (r"^(method|methods|methodology|approach)$", "Methods"),
    (r"^(experiment|experiments|evaluation)$", "Experiments"),
    (r"^(result|results|findings)$", "Results"),
    (r"^(discussion|analysis)$", "Discussion"),
    (r"^(conclusion|conclusions)$", "Conclusion"),
    (r"^(reference|references|bibliography)$", "References"),
]


def _clean_text(value: str) -> str:
    text = value.replace("-\n", "")
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _canonicalize_section(line: str) -> str | None:
    normalized = line.lower().strip().rstrip(":")
    normalized = re.sub(r"^\d+(?:\.\d+)*\s+", "", normalized)
    normalized = re.sub(r"\s+", " ", normalized)

    for pattern, name in CANONICAL_SECTIONS:
        if re.match(pattern, normalized):
            return name
    return None


def _is_heading_line(line: str) -> bool:
    if not line:
        return False

    stripped = line.strip()
    if len(stripped) > 100:
        return False

    if stripped.endswith("."):
        return False

    if sum(ch.isalpha() for ch in stripped) < 3:
        return False

    canonical = _canonicalize_section(stripped)
    if canonical is not None:
        return True

    words = [w for w in re.split(r"\s+", stripped) if w]
    if not words or len(words) > 8:
        return False

    title_like = sum(1 for w in words if w[:1].isupper()) >= max(1, int(len(words) * 0.7))
    uppercase_like = stripped.upper() == stripped and len(words) <= 6
    numbered_heading = bool(re.match(r"^\d+(?:\.\d+)*\s+", stripped))
    return title_like or uppercase_like or numbered_heading


def parse_pdf(raw_bytes: bytes) -> dict:
    if not raw_bytes:
        return {
            "title": "Untitled",
            "size": 0,
            "page_count": 0,
            "sections": [],
        }

    document = fitz.open(stream=raw_bytes, filetype="pdf")
    page_count = len(document)
    sections: "OrderedDict[str, dict]" = OrderedDict()
    current_section = "Front Matter"
    sections[current_section] = {"name": current_section, "page_start": 1, "paragraphs": []}

    for page_index in range(len(document)):
        page_number = page_index + 1
        page = document.load_page(page_index)
        blocks = sorted(page.get_text("blocks"), key=lambda block: (block[1], block[0]))

        for block in blocks:
            raw_block = block[4] if len(block) > 4 else ""
            if not raw_block.strip():
                continue

            lines = [_clean_text(line) for line in raw_block.splitlines() if _clean_text(line)]
            if not lines:
                continue

            # If a heading appears at the start of the block, switch sections.
            leading = lines[0]
            if _is_heading_line(leading):
                current_section = _canonicalize_section(leading) or leading.strip().rstrip(":")
                if current_section not in sections:
                    sections[current_section] = {
                        "name": current_section,
                        "page_start": page_number,
                        "paragraphs": [],
                    }
                lines = lines[1:]

            if not lines:
                continue

            paragraph_text = _clean_text(" ".join(lines))
            if not paragraph_text:
                continue

            sections[current_section]["paragraphs"].append(
                {
                    "page": page_number,
                    "text": paragraph_text,
                }
            )

    metadata = document.metadata or {}
    parsed_title = metadata.get("title") or ""

    if not parsed_title:
        first_page_text = _clean_text(document.load_page(0).get_text("text")) if page_count else ""
        words = first_page_text.split(" ")[:12]
        parsed_title = " ".join(words) if words else "Untitled"

    document.close()

    return {
        "title": parsed_title or "Untitled",
        "size": len(raw_bytes),
        "page_count": page_count,
        "sections": list(sections.values()),
    }
