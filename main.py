import os
import json
from pathlib import Path
from utils import extract_headings

INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")

def main():
    pdf_files = list(INPUT_DIR.glob("*.pdf"))
    if not pdf_files:
        print("No PDF files found in input directory.")
        return
    
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    for pdf_file in pdf_files:
        print(f"Processing: {pdf_file.name}")
        title, headings = extract_headings(pdf_file)
    
        output_data = {
            "title": title,
            "outline": headings
        }

        output_file = OUTPUT_DIR / f"{pdf_file.stem}.json"
        with open(output_file, "w") as f:
            json.dump(output_data, f, indent=2)

if __name__ == "__main__":
    main()