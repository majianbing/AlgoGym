from dataclasses import dataclass


@dataclass(frozen=True)
class TextChunk:
    index: int
    text: str
    heading: str | None = None


def chunk_markdown(markdown: str, max_chars: int = 1800) -> list[TextChunk]:
    """Chunk markdown by level-two sections, preserving preface text if present."""
    chunks: list[TextChunk] = []
    heading: str | None = None
    buffer: list[str] = []

    def flush() -> None:
        nonlocal buffer
        text = "\n".join(buffer).strip()
        if text:
            chunks.append(TextChunk(index=len(chunks), text=text, heading=heading))
        buffer = []

    for raw_line in markdown.splitlines():
        line = raw_line.rstrip()
        if line.startswith("## ") and not line.startswith("###"):
            flush()
            heading = line.removeprefix("##").strip() or None
            buffer.append(line)
            continue

        current_size = sum(len(item) + 1 for item in buffer)
        if buffer and current_size + len(line) + 1 > max_chars:
            flush()
        buffer.append(line)

    flush()
    return chunks
