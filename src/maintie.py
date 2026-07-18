"""MaintIE real work-order corpus loader.

MaintIE (Bikaun et al., LREC-COLING 2024, MIT licence, github.com/nlp-tlp/maintie)
provides 1,076 expert double-annotated (gold) and 7,000 expert-reviewed (silver)
REAL maintenance work orders from mining, rail and heavy industry. We use:
  * gold  -> train/eval our entity extractor (the published benchmark)
  * silver -> field-intelligence statistics + retrieval corpus
"""
import json
import os

MAINTIE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           "external", "maintie", "data")

TOP_CLASSES = ["PhysicalObject", "State", "Process", "Activity", "Property"]


def available():
    return os.path.exists(os.path.join(MAINTIE_DIR, "gold_release.json"))


def load(split):
    path = os.path.join(MAINTIE_DIR, f"{split}_release.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def top_class(entity_type):
    return entity_type.split("/")[0]


def to_bio(record):
    """Convert a MaintIE record to (tokens, BIO labels at top-class level)."""
    tokens = record["tokens"]
    labels = ["O"] * len(tokens)
    for ent in record.get("entities", []):
        cls = top_class(ent["type"])
        if cls not in TOP_CLASSES:
            continue
        s, e = ent["start"], ent["end"]
        if s >= len(tokens):
            continue
        labels[s] = f"B-{cls}"
        for i in range(s + 1, min(e, len(tokens))):
            labels[i] = f"I-{cls}"
    return tokens, labels


def clean_text(record):
    """Human-readable text of a work order (drop the <id> placeholder token)."""
    return " ".join(t for t in record["tokens"] if t != "<id>").strip()
