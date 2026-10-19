
from pathlib import Path
import json

import chromadb
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent
CHUNKS_FILE = BASE_DIR / "processed_data" / "chunks.json"
DB_DIR = BASE_DIR / "vector_db"

COLLECTION_NAME = "ism_knowledge"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def main():
    if not CHUNKS_FILE.exists():
        print("ERROR: chunks.json not found.")
        print("Run python chunking.py first.")
        return

    with open(CHUNKS_FILE, "r", encoding="utf-8") as file:
        chunks = json.load(file)

    if not chunks:
        print("ERROR: No chunks found.")
        return

    print(f"Loaded {len(chunks)} chunks.")
    print("Loading embedding model...")

    model = SentenceTransformer(EMBEDDING_MODEL)

    print("Creating vector database...")
    client = chromadb.PersistentClient(path=str(DB_DIR))

    # Rebuild this project's collection on each run
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    batch_size = 50

    for start in range(0, len(chunks), batch_size):
        batch = chunks[start:start + batch_size]

        texts = [item["text"] for item in batch]
        embeddings = model.encode(
            texts,
            normalize_embeddings=True,
        ).tolist()

        collection.add(
            ids=[str(item["chunk_id"]) for item in batch],
            documents=texts,
            embeddings=embeddings,
            metadatas=[
                {
                    "unit": item["unit"],
                    "source_file": item["source_file"],
                    "page_number": item["page_number"],
                    "chunk_id": item["chunk_id"],
                }
                for item in batch
            ],
        )

        print(f"Stored {min(start + batch_size, len(chunks))}/{len(chunks)} chunks")

    print("\nVector database created successfully!")
    print(f"Stored chunks: {collection.count()}")
    print(f"Database location: {DB_DIR}")


if __name__ == "__main__":
    main()
