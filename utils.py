import fitz  # PyMuPDF

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
                            continue  # ignore empty or too short
                        text_info.append({
                            "text": text,
                            "size": round(span["size"], 2),
                            "font": span["font"],
                            "bold": "bold" in span["font"].lower(),
                            "page": page_num
                        })
    except Exception as e:
        print(f"Error processing PDF content: {e}")
        doc.close()
        return "Untitled", []

    if not text_info:
        doc.close()
        return "Untitled", []

    # Sort by size descending
    heading_candidates = sorted(text_info, key=lambda x: -x["size"])

    # Get top 3 unique sizes (assumed to be H1, H2, H3)
    unique_sizes = sorted({item["size"] for item in heading_candidates}, reverse=True)[:3]

    def classify(size):
        if not unique_sizes:
            return None
        if size >= unique_sizes[0]:
            return "H1"
        elif len(unique_sizes) > 1 and size >= unique_sizes[1]:
            return "H2"
        elif len(unique_sizes) > 2 and size >= unique_sizes[2]:
            return "H3"
        else:
            return None

    outline = []
    seen = set()
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