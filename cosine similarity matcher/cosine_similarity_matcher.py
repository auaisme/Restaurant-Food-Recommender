import numpy as np
from typing import List, Tuple
import json
import csv

CONSOLE_COLOR = {
    "RED": "\033[91m",
    "GREEN": "\033[92m",
    "YELLOW": "\033[93m",
    "BLUE": "\033[94m",
    "MAGENTA": "\033[95m",
    "CYAN": "\033[96m",
    "RESET": "\033[0m"
}

def vector_interpretor(item_vector, csv_path):
    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Read first line only

    components = {}
    i = 0

    for field in headers:
        if field == "name": continue
        components[field] = int(item_vector[i])
        i = i + 1

    return components

def load_menu_vectors(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        menu_vectors = json.load(f)
    return menu_vectors

def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    # ^ Avoid dividing by zero
    if np.linalg.norm(vec1) == 0 or np.linalg.norm(vec2) == 0:
        return 0.0
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def get_top_matches(cart_vector: List[float], combo_vectors: List[dict], top_k: int = 3, min_score=0.5) -> List[Tuple[str, float]]:
    SCORE_INDEX_IN_RECOMMENDATION = 1
    
    cart_vec = np.array(cart_vector)

    scores = []
    for combo in combo_vectors:
        combo_vec = np.array(combo['vector'])

        # Optional: zero out price or remove it
        combo_vec[-1] = 0
        sim = cosine_similarity(cart_vec, combo_vec)
        scores.append((combo['combo_id'], sim))

    # Sort by similarity descending
    scores.sort(key=lambda x: x[1], reverse=True)

    print(scores)

    scores = scores[:top_k]

    recommendations = [] # TODO Replace this with in-memory solution
    for recommendation in scores:
        print(f"\n{CONSOLE_COLOR['MAGENTA']}{recommendation}{CONSOLE_COLOR['RESET']}")
        if recommendation[SCORE_INDEX_IN_RECOMMENDATION] < min_score:
            continue
        recommendations.append(recommendation)
    
    print(recommendations)

    return recommendations

def get_recommendations(cart_vector, menu_vectors, count = 3, min_score=0.5):
    # Run the matcher
    top_matches = get_top_matches(cart_vector, menu_vectors, top_k=3, min_score=min_score)

    # Print results
    for combo_id, score in top_matches:
        print(f"{CONSOLE_COLOR['CYAN']}{combo_id}{CONSOLE_COLOR['RESET']}: {CONSOLE_COLOR['GREEN']}{score:.3f}{CONSOLE_COLOR['RESET']}")
    
    return top_matches

menu_vectors = load_menu_vectors(json_path="../menu formator/test_menu_1.json")
print(json.dumps(menu_vectors, indent=2))

# ? Your cart vector: e.g., 2 chicken pieces and 2 burgers
# ^ The last value (price) is 0 or removed to avoid skewing similarity
cart_vector = np.array([2, 2, 0, 0, 0.0])

print(f"Cart Vector: {vector_interpretor(cart_vector, '../menu formator/test_menu_1.csv')}")
recommendations = get_recommendations(cart_vector=cart_vector, menu_vectors=menu_vectors, count=3, min_score=0.80)
