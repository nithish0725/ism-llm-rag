
from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "processed_data" / "extracted_pages.json"
OUTPUT_FILE = BASE_DIR / "processed_data" / "chunks.json"

# Approximate chunk size and overlap, measured in words
CHUNK_SIZE = 250
CHUNK_OVERLAP = 40


def split_into_chunks(text):
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = min(start + CHUNK_SIZE, len(words))
        chunk_text = " ".join(words[start:end])

        if chunk_text.strip():
            chunks.append(chunk_text)

        if end == len(words):
            break

        start = end - CHUNK_OVERLAP

    return chunks


def main():
    if not INPUT_FILE.exists():
        print(f"ERROR: Input file not found: {INPUT_FILE}")
        print("Run pdf_processor.py first.")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        pages = json.load(file)

    all_chunks = []
    chunk_id = 0

    for page in pages:
        text = page.get("text", "")
        page_chunks = split_into_chunks(text)

        for chunk_text in page_chunks:
            chunk_id += 1

            all_chunks.append({
                "chunk_id": chunk_id,
                "unit": page["unit"],
                "source_file": page["source_file"],
                "page_number": page["page_number"],
                "text": chunk_text,
            })

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(all_chunks, file, ensure_ascii=False, indent=2)

    print("Chunking completed successfully!")
    print(f"Pages processed: {len(pages)}")
    print(f"Total chunks created: {len(all_chunks)}")
    print(f"Output saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
