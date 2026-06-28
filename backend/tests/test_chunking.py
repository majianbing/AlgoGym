from app.services.chunking import chunk_markdown


def test_chunk_markdown_tracks_level_two_headings() -> None:
    chunks = chunk_markdown("# Patterns\n\n## Binary Search\n\nUse monotonic predicates.")

    assert len(chunks) == 2
    assert chunks[1].heading == "Binary Search"
    assert "monotonic predicates" in chunks[1].text


def test_chunk_markdown_splits_large_level_two_sections() -> None:
    markdown = "## Sliding Window\n" + "\n".join(["expand and shrink"] * 200)

    chunks = chunk_markdown(markdown, max_chars=120)

    assert len(chunks) > 1
    assert all(chunk.text for chunk in chunks)
