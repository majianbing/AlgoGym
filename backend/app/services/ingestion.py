from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.config import Settings
from app.models import Document
from app.services.chunking import chunk_markdown
from app.services.vector_store import KnowledgeVectorStore


def validate_markdown_upload(upload: UploadFile) -> str:
    filename = Path(upload.filename or "").name
    if not filename:
        raise ValueError("Missing filename")
    if Path(filename).suffix.lower() not in {".md", ".markdown"}:
        raise ValueError("Only markdown files are supported")
    return filename


async def save_markdown_upload(upload: UploadFile, settings: Settings) -> tuple[str, str, str]:
    filename = validate_markdown_upload(upload)
    raw = await upload.read()
    text = raw.decode("utf-8")

    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)
    stored_name = f"{uuid4().hex}-{filename}"
    path = upload_dir / stored_name
    path.write_text(text, encoding="utf-8")
    return filename, str(path), text


def ingest_document(document: Document, settings: Settings) -> int:
    text = document.content or Path(document.source_path).read_text(encoding="utf-8")
    chunks = chunk_markdown(text)
    store = KnowledgeVectorStore(settings)
    return store.upsert_document(document, chunks)
