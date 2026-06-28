from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlmodel import Session, select

from app.config import get_settings
from app.database import get_session
from app.models import Document, DocumentCreate, utc_now
from app.services.ingestion import ingest_document, save_markdown_upload

router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("", response_model=list[Document])
def list_documents(session: Session = Depends(get_session)) -> list[Document]:
    return list(session.exec(select(Document).order_by(Document.created_at.desc())).all())


@router.post("", response_model=Document)
def create_document(
    payload: DocumentCreate, session: Session = Depends(get_session)
) -> Document:
    document = Document.model_validate(payload)
    session.add(document)
    session.commit()
    session.refresh(document)
    return document


@router.post("/upload", response_model=Document)
async def upload_document(
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
) -> Document:
    try:
        filename, path = await save_markdown_upload(file, get_settings())
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=400, detail="File must be UTF-8 markdown") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    document = Document(filename=filename, title=filename, source_path=path)
    session.add(document)
    session.commit()
    session.refresh(document)

    try:
        chunks_count = ingest_document(document, get_settings())
    except Exception as exc:
        document.status = "ingestion_failed"
        document.updated_at = utc_now()
        session.add(document)
        session.commit()
        session.refresh(document)
        raise HTTPException(
            status_code=502,
            detail=f"Saved file, but ingestion failed: {exc}",
        ) from exc

    document.status = "ingested"
    document.chunks_count = chunks_count
    document.updated_at = utc_now()
    session.add(document)
    session.commit()
    session.refresh(document)
    return document


@router.post("/{document_id}/ingest", response_model=Document)
def ingest_existing_document(
    document_id: int, session: Session = Depends(get_session)
) -> Document:
    document = session.get(Document, document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    try:
        chunks_count = ingest_document(document, get_settings())
    except Exception as exc:
        document.status = "ingestion_failed"
        document.updated_at = utc_now()
        session.add(document)
        session.commit()
        raise HTTPException(status_code=502, detail=f"Ingestion failed: {exc}") from exc
    document.status = "ingested"
    document.chunks_count = chunks_count
    document.updated_at = utc_now()
    session.add(document)
    session.commit()
    session.refresh(document)
    return document


@router.patch("/{document_id}", response_model=Document)
def update_document_status(
    document_id: int, status: str, session: Session = Depends(get_session)
) -> Document:
    document = session.get(Document, document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    document.status = status
    document.updated_at = utc_now()
    session.add(document)
    session.commit()
    session.refresh(document)
    return document
