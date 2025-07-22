from sklearn.cluster import KMeans
from collections import Counter
import numpy as np

def assign_heading_levels(spans, embeddings):
    """Assign heading levels using improved clustering with visual features."""
    if not spans or not embeddings:
        return []
    features = []
    for span, emb in zip(spans, embeddings):
        extra = np.array([
            span["size"] / 20.0,
            span["x"] / 600.0,
            1.0 if span["bold"] else 0.0,
            1.0 / span["page"]
        ])
        combined_features = np.concatenate([emb / np.linalg.norm(emb), extra])
        features.append(combined_features)
    features = np.array(features)
    n_clusters = min(4, max(2, len(set(span["size"] for span in spans))))
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10).fit(features)
    labels = kmeans.labels_
    cluster_avg_sizes = {}
    for i in range(n_clusters):
        cluster_spans = [spans[j] for j, label in enumerate(labels) if label == i]
        if cluster_spans:
            cluster_avg_sizes[i] = np.mean([s["size"] for s in cluster_spans])
    sorted_clusters = sorted(cluster_avg_sizes.items(), key=lambda x: x[1], reverse=True)
    level_map = {cluster_id: f"H{i+1}" for i, (cluster_id, _) in enumerate(sorted_clusters)}
    output = []
    for span, label in zip(spans, labels):
        output.append({**span, "level": level_map[label]})
    return output

def score_title(spans):
    """
    Find the best title candidate using improved heuristics:
    - Appears early in document (page ≤ 2)
    - Appropriate length (not too short/long)
    - Large font size relative to document
    - Bold formatting
    - Center or left alignment
    - Not all caps (often indicates headers/footers)
    """
    if not spans:
        return "Untitled"
    candidates = [
        s for s in spans 
        if (4 <= len(s["text"]) <= 100 and
            s["page"] <= 2 and
            not s["text"].isupper() and
            not s["text"].isdigit())
    ]
    if not candidates:
        return "Untitled"
    all_sizes = [s["size"] for s in spans]
    avg_size = np.mean(all_sizes)
    max_size = max(all_sizes)
    best = None
    best_score = -1
    for item in candidates:
        score = 0
        if item["page"] == 1:
            score += 3
        elif item["page"] == 2:
            score += 1
        size_ratio = item["size"] / avg_size
        if size_ratio > 1.5:
            score += 3
        elif size_ratio > 1.2:
            score += 2
        elif size_ratio > 1.0:
            score += 1
        if item["bold"]:
            score += 2
        if 100 <= item["x"] <= 400:
            score += 2
        elif item["x"] < 100:
            score += 1
        text_len = len(item["text"])
        if 10 <= text_len <= 50:
            score += 2
        elif 5 <= text_len <= 80:
            score += 1
        if item["y"] < 200:
            score += 1
        if score > best_score:
            best = item
            best_score = score

    return best["text"] if best else "Untitled"