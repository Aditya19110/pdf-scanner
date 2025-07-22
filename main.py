from pathlib import Path
import os
import json
from utils import extract_text_spans
from classify import get_embedding
from cluster import assign_heading_levels, score_title

os.environ["TOKENIZERS_PARALLELISM"] = "false"
INPUT_DIR = Path("input")
INPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def main():
    for pdf_file in INPUT_DIR.glob("*.pdf"):
        print(f"Reading: {pdf_file.name}")
        spans = extract_text_spans(pdf_file)
        if not spans:
            print(f"Skipping {pdf_file.name} — no valid spans found.")
            continue
        try:
            embeddings = [get_embedding(span["text"]) for span in spans]
        except Exception as e:
            print(f"Embedding failed on {pdf_file.name}: {e}")
            continue
        headings = assign_heading_levels(spans, embeddings)
        headings = [
            h for h in headings
            if len(h["text"]) > 3 and len(h["text"].split()) <= 15
        ]
        headings = sorted(headings, key=lambda h: (h["page"], h["y"], h["x"]))
        seen = set()
        unique_headings = []
        for h in headings:
            key = (h["text"].lower().strip(), h["page"])
            if key not in seen:
                seen.add(key)
                unique_headings.append(h)
        headings = unique_headings
        if not headings:
            print(f"Skipping {pdf_file.name} — no valid headings after filtering.")
            continue
        title = score_title(headings)
        result = {
            "title": title,
            "outline": [
                {
                    "level": h["level"], 
                    "text": h["text"], 
                    "page": h["page"],
                    "position": {"x": h["x"], "y": h["y"]}
                }
                for h in headings
            ],
            "metadata": {
                "total_headings": len(headings),
                "pages_processed": max(h["page"] for h in headings) if headings else 0,
                "font_sizes_detected": sorted(list(set(h["size"] for h in headings)), reverse=True)
            }
        }
        out_file = OUTPUT_DIR / f"{pdf_file.stem}.json"
        try:
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"Processed: {pdf_file.name} → {out_file.name}")
            print(f"Found {len(headings)} headings, Title: '{title}'")
        except Exception as e:
            print(f"Failed to save {out_file}: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProcess interrupted by user")
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()