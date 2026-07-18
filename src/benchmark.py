"""Entity-extraction benchmark on the MaintIE gold corpus.

Trains a token classifier (windowed lexical features -> logistic regression)
on 80% of the expert-annotated gold work orders and reports token-level
precision/recall/F1 on the held-out 20%. Also derives field-intelligence
statistics from the silver corpus annotations.

Run as a script to (re)generate data/benchmark_results.json, which the app
displays — so the demo never waits on training.
"""
import json
import os
import re
from collections import Counter

from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

from . import maintie

OUT_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "data", "benchmark_results.json")


def _feats(tokens, i):
    w = tokens[i]
    lw = w.lower()
    f = {"w": lw, "suf3": lw[-3:], "pre2": lw[:2], "isdigit": w.isdigit(),
         "hasdigit": bool(re.search(r"\d", w)), "len": min(len(w), 8)}
    f["prev"] = tokens[i - 1].lower() if i > 0 else "<s>"
    f["next"] = tokens[i + 1].lower() if i < len(tokens) - 1 else "</s>"
    f["prev2"] = tokens[i - 2].lower() if i > 1 else "<s>"
    return f


def run():
    gold = maintie.load("gold")
    X_rec, y_rec = [], []
    for r in gold:
        toks, labs = maintie.to_bio(r)
        X_rec.append([_feats(toks, i) for i in range(len(toks))])
        y_rec.append(labs)
    Xtr_r, Xte_r, ytr_r, yte_r = train_test_split(X_rec, y_rec, test_size=0.2,
                                                  random_state=42)
    Xtr = [f for rec in Xtr_r for f in rec]
    ytr = [l for rec in ytr_r for l in rec]
    Xte = [f for rec in Xte_r for f in rec]
    yte = [l for rec in yte_r for l in rec]

    vec = DictVectorizer()
    Xtr_v = vec.fit_transform(Xtr)
    Xte_v = vec.transform(Xte)
    clf = LogisticRegression(max_iter=400, C=2.0, n_jobs=-1)
    clf.fit(Xtr_v, ytr)
    pred = clf.predict(Xte_v)

    # collapse BIO -> class for a per-class report judges can read
    def collapse(seq):
        return [l.split("-", 1)[1] if "-" in l else l for l in seq]

    rep = classification_report(collapse(yte), collapse(list(pred)),
                                output_dict=True, zero_division=0)

    # field intelligence from silver annotations (7,000 real MWOs)
    silver = maintie.load("silver")
    objs, states, top_pairs = Counter(), Counter(), Counter()
    for r in silver:
        toks = r["tokens"]
        ents = r.get("entities", [])
        rec_objs, rec_states = [], []
        for e in ents:
            phrase = " ".join(toks[e["start"]:e["end"]]).lower()
            cls = maintie.top_class(e["type"])
            if not phrase or "<id>" in phrase:
                continue
            if cls == "PhysicalObject":
                objs[phrase] += 1
                rec_objs.append(phrase)
            elif cls == "State":
                states[phrase] += 1
                rec_states.append(phrase)
        for o in set(rec_objs):
            for s in set(rec_states):
                top_pairs[f"{o} — {s}"] += 1

    results = {
        "corpus": "MaintIE (Bikaun et al., LREC-COLING 2024, MIT licence)",
        "gold_records": len(gold),
        "silver_records": len(silver),
        "train_records": len(Xtr_r),
        "test_records": len(Xte_r),
        "test_tokens": len(yte),
        "per_class": {cls: {"precision": round(rep[cls]["precision"], 3),
                            "recall": round(rep[cls]["recall"], 3),
                            "f1": round(rep[cls]["f1-score"], 3),
                            "support": int(rep[cls]["support"])}
                      for cls in maintie.TOP_CLASSES + ["O"] if cls in rep},
        "macro_f1": round(rep["macro avg"]["f1-score"], 3),
        "accuracy": round(rep["accuracy"], 3),
        "top_failed_objects": objs.most_common(12),
        "top_states": states.most_common(10),
        "top_object_state_pairs": top_pairs.most_common(12),
    }
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=1)
    return results


def load_results():
    if not os.path.exists(OUT_PATH):
        return None
    with open(OUT_PATH, encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    r = run()
    print(f"gold={r['gold_records']} silver={r['silver_records']} "
          f"macroF1={r['macro_f1']} acc={r['accuracy']}")
    for cls, m in r["per_class"].items():
        print(f"  {cls:16s} P={m['precision']:.2f} R={m['recall']:.2f} F1={m['f1']:.2f} n={m['support']}")
