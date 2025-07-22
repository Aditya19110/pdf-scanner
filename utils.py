import fitz  
import re

def extract_text_spans(pdf_path):
    """Extract text spans with position and formatting information from PDF."""
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Error opening PDF {pdf_path}: {e}")
        return []
    spans = []

    try:
        for page_num, page in enumerate(doc, start=1):
            blocks = page.get_text("dict")["blocks"]
            for block in blocks:
                if "lines" not in block:
                    continue
                    
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        text = span["text"].strip()
                        if (len(text) < 3 or 
                            len(text.split()) > 12 or 
                            re.match(r'^\d+$', text) or
                            text.isspace()):
                            continue
                        is_bold = (span.get("flags", 0) & 2**4) != 0 or "bold" in span["font"].lower()
                        spans.append({
                            "text": text,
                            "size": round(span["size"], 2),
                            "font": span["font"],
                            "bold": is_bold,
                            "page": page_num,
                            "x": round(span["bbox"][0], 2),  
                            "y": round(span["bbox"][1], 2),  
                            "width": round(span["bbox"][2] - span["bbox"][0], 2), 
                            "height": round(span["bbox"][3] - span["bbox"][1], 2) 
                        })
    except Exception as e:
        print(f"Error processing PDF content: {e}")
    finally:
        doc.close()
    
    return spans