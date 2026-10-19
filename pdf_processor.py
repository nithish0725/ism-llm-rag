
from pathlib import Path
import json
import fitz  # PyMuPDF

# Find the main project folder
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "processed_data"

# Create an output folder automatically
OUTPUT_DIR.mkdir(exist_ok=True)

pdf_files = [
    "Unit1.pdf",
    "Unit2.pdf",
    "Unit3.pdf",
    "Unit4.pdf",
]

all_pages = []

for filename in pdf_files:
    pdf_path = DATA_DIR / filename

    if not pdf_path.exists():
        print(f"ERROR: Cannot find {filename} in the data folder.")
        continue

    print(f"\nReading {filename}...")

    try:
        with fitz.open(pdf_path) as pdf:
            extracted_pages = 0

            for page_number, page in enumerate(pdf, start=1):
                text = page.get_text("text").strip()

                if text:
                    all_pages.append({
                        "unit": filename.replace(".pdf", ""),
                        "source_file": filename,
                        "page_number": page_number,
                        "text": text,
                    })
                    extracted_pages += 1

            print(f"Total PDF pages: {len(pdf)}")
            print(f"Pages with extracted text: {extracted_pages}")

    except Exception as error:
        print(f"ERROR reading {filename}: {error}")

# Save the extracted text and page references
output_path = OUTPUT_DIR / "extracted_pages.json"

with open(output_path, "w", encoding="utf-8") as file:
    json.dump(all_pages, file, ensure_ascii=False, indent=2)

print("\nPDF processing finished.")
print(f"Total pages with text: {len(all_pages)}")
print(f"Output saved to: {output_path}")
