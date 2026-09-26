# add_categories.py - one-shot script to add category field (260927HHMM)
import json
from pathlib import Path

REGISTRY = Path(__file__).parent / "registry" / "tasks.json"

CATEGORIES = {
    "001": "read",
    "002": "clean", "003": "clean", "010": "clean", "014": "clean",
    "005": "transform", "006": "transform", "007": "transform", "008": "transform",
    "009": "transform", "011": "transform", "012": "transform", "013": "transform",
    "016": "transform", "017": "transform", "018": "transform",
    "019": "convert",
    "020": "analyze", "029": "analyze",
    "015": "deliver", "022": "deliver", "023": "deliver",
    "021": "ops", "025": "ops", "026": "ops", "027": "ops", "028": "ops", "030": "ops",
    # 004 combine_excel - transform
    "004": "transform",
    # 024 file_picker - exclude (human tool)
    "024": "dev",
}

def main():
    with open(REGISTRY, encoding="utf-8") as f:
        data = json.load(f)

    updated = 0
    for tid, task in data.items():
        if tid in CATEGORIES:
            task["category"] = CATEGORIES[tid]
            updated += 1

    with open(REGISTRY, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Updated {updated} tasks with categories.")

if __name__ == "__main__":
    main()