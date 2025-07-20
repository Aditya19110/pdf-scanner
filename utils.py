import fitz
import re
from collections import Counter

def extract_headings(pdf_path):
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Error opening PDF {pdf_path}: {e}")
        return "Untitled", []

    text_info = []

    try:
        for page_num, page in enumerate(doc, start=1):
            blocks = page.get_text("dict")["blocks"]
            for block in blocks:
                if "lines" not in block:
                    continue
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        text = span["text"].strip()
                        if not text or len(text) < 3:
                            continue
                        if re.match(r'^\d+$', text):
                            continue
                        text_info.append({
                            "text": text,
                            "size": round(span["size"], 1),
                            "font": span["font"],
                            "bold": span.get("flags", 0) & 2 != 0,
                            "page": page_num
                        })
    except Exception as e:
        print(f"Error processing PDF content: {e}")
        doc.close()
        return "Untitled", []

    if not text_info:
        doc.close()
        return "Untitled", []

    # Count frequency of each font size
    size_counts = Counter([item["size"] for item in text_info])
    # Pick most frequent large font sizes
    common_sizes = sorted(size_counts.items(), key=lambda x: (-x[0], -x[1]))
    top_sizes = [size for size, _ in common_sizes[:3]]

    def classify(size):
        if not top_sizes:
            return None
        if abs(size - top_sizes[0]) < 0.5:
            return "H1"
        elif len(top_sizes) > 1 and abs(size - top_sizes[1]) < 0.5:
            return "H2"
        elif len(top_sizes) > 2 and abs(size - top_sizes[2]) < 0.5:
            return "H3"
        else:
            return None

    heading_candidates = sorted(text_info, key=lambda x: -x["size"])
    seen = set()
    outline = []
    for item in heading_candidates:
        level = classify(item["size"])
        key = (item["text"], item["page"])
        if level and key not in seen:
            seen.add(key)
            outline.append({
                "level": level,
                "text": item["text"],
                "page": item["page"]
            })

    doc.close()
    title = next((h["text"] for h in outline if h["level"] == "H1"), "Untitled")
    return title, outline
