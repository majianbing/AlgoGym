from pathlib import Path

import chromadb

from app.config import Settings
from app.models import Document
from app.services.chunking import TextChunk
from app.services.embeddings import EmbeddingService

COLLECTION_NAME = "algogym_knowledge"


class KnowledgeVectorStore:
    def __init__(self, settings: Settings):
        self.settings = settings
        Path(settings.chroma_path).mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=settings.chroma_path)
        self.collection = self.client.get_or_create_collection(name=COLLECTION_NAME)
        self.embeddings = EmbeddingService(settings)

    def upsert_document(self, document: Document, chunks: list[TextChunk]) -> int:
        if not chunks:
            return 0

        ids = [f"document:{document.id}:chunk:{chunk.index}" for chunk in chunks]
        documents = [chunk.text for chunk in chunks]
        embeddings = self.embeddings.embed(documents)
        metadatas = [
            {
                "document_id": document.id,
                "filename": document.filename,
                "chunk_index": chunk.index,
                "heading": chunk.heading or "",
            }
            for chunk in chunks
        ]

        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )
        return len(chunks)

    def query(self, query: str, limit: int = 5) -> list[dict[str, object]]:
        try:
            embeddings = self.embeddings.embed([query])
            if not embeddings:
                return []
            results = self.collection.query(
                query_embeddings=embeddings,
                n_results=limit,
                include=["documents", "metadatas", "distances"],
            )
        except Exception:
            return []
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]
        return [
            {"text": text, "metadata": metadata, "distance": distance}
            for text, metadata, distance in zip(documents, metadatas, distances)
        ]
