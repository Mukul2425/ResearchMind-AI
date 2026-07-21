from __future__ import annotations

from uuid import uuid4

from app.models.document import DocumentChunk


def _finalize_chunk(
    chunks: list[DocumentChunk],
    document_id: str,
    title: str,
    section: str,
    paragraphs: list[dict],
) -> None:
    if not paragraphs:
        return

    chunk_text = "\n\n".join(p["text"] for p in paragraphs if p.get("text"))
    if not chunk_text.strip():
        return

    chunks.append(
        DocumentChunk(
            chunk_id=str(uuid4()),
            document_id=document_id,
            text=chunk_text,
            page=paragraphs[0].get("page"),
            page_end=paragraphs[-1].get("page"),
            section=section,
            title=title,
        )
    )


def chunk_document(
    document_id: str,
    parsed_document: dict,
    max_chars: int = 1200,
    overlap_chars: int = 180,
) -> list[DocumentChunk]:
    title = parsed_document.get("title") or "Untitled"
    sections = parsed_document.get("sections") or []

    all_chunks: list[DocumentChunk] = []

    for section in sections:
        section_name = section.get("name") or "Unknown Section"
        paragraphs = section.get("paragraphs") or []

        current: list[dict] = []
        current_size = 0

        for paragraph in paragraphs:
            text = (paragraph.get("text") or "").strip()
            if not text:
                continue

            candidate_size = current_size + len(text)
            if current and candidate_size > max_chars:
                _finalize_chunk(all_chunks, document_id, title, section_name, current)

                if overlap_chars > 0:
                    overlap: list[dict] = []
                    overlap_size = 0
                    for prev in reversed(current):
                        prev_text = prev.get("text", "")
                        overlap_size += len(prev_text)
                        overlap.insert(0, prev)
                        if overlap_size >= overlap_chars:
                            break
                    current = overlap
                    current_size = sum(len(p.get("text", "")) for p in current)
                else:
                    current = []
                    current_size = 0

            current.append({"page": paragraph.get("page"), "text": text})
            current_size += len(text)

        _finalize_chunk(all_chunks, document_id, title, section_name, current)

    return all_chunks
