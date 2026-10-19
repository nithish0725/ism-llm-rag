
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / "vector_db"

COLLECTION_NAME = "ism_knowledge"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def search_ism(question, top_k=5):
    """Retrieve relevant passages from the four ISM unit PDFs."""

    if not question.strip():
        print("Please enter a question.")
        return

    client = chromadb.PersistentClient(path=str(DB_DIR))

    try:
        collection = client.get_collection(COLLECTION_NAME)
    except Exception as error:
        print("Could not open the ISM vector database.")
        print("Run python build_vector_db.py first.")
        print(f"Details: {error}")
        return

    print("Loading the embedding model...")
    model = SentenceTransformer(EMBEDDING_MODEL)

    question_embedding = model.encode(
        [question],
        normalize_embeddings=True,
    ).tolist()

    result_count = min(top_k, collection.count())

    if result_count == 0:
        print("The ISM knowledge base is empty.")
        return

    results = collection.query(
        query_embeddings=question_embedding,
        n_results=result_count,
        include=["documents", "metadatas", "distances"],
    )

    print("\nRelevant ISM passages")
    print("=" * 60)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for index, (text, metadata, distance) in enumerate(
        zip(documents, metadatas, distances),
        start=1,
    ):
        print(f"\nResult {index}")
        print(f"Unit: {metadata['unit']}")
        print(f"PDF: {metadata['source_file']}")
        print(f"Page: {metadata['page_number']}")
        print(f"Distance: {distance:.4f}")
        print(f"Content:\n{text}")
        print("-" * 60)


if __name__ == "__main__":
    question = input("Enter an ISM question: ")
    search_ism(question)

