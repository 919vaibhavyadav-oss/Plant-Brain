"""Retrieval layer: TF-IDF vector index over every ingested chunk.

Kept dependency-light and instant to build so the demo never waits on model
downloads. The interface (search -> ranked chunks with scores) is what an
embedding model would slot into in production.
"""
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .ingest import TAG_RE


class Index:
    def __init__(self, chunks):
        self.chunks = chunks
        self.vec = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True,
                                   stop_words="english", max_features=50000)
        self.mat = self.vec.fit_transform([c.text for c in chunks])

    # narrative sources carry more answer-density than routine transactional rows
    TYPE_BOOST = {"incident": 1.30, "sop": 1.25, "regulation": 1.20,
                  "standard": 1.15, "inspection": 1.10, "work_order": 1.00,
                  "equipment": 0.90, "field_wo": 0.80}

    def search(self, query, k=6, doc_types=None):
        qv = self.vec.transform([query])
        sims = cosine_similarity(qv, self.mat).ravel()
        boosts = np.array([self.TYPE_BOOST.get(c.doc_type, 1.0) for c in self.chunks])
        # entity-aware retrieval: a query naming a specific asset strongly
        # prefers records about that asset over generic look-alike text
        qtags = set(TAG_RE.findall(query))
        if qtags:
            tag_boost = np.array([1.6 if qtags & set(c.equipment_tags) else 1.0
                                  for c in self.chunks])
            boosts = boosts * tag_boost
        sims = sims * boosts
        order = np.argsort(-sims)
        out = []
        for i in order:
            c = self.chunks[i]
            if doc_types and c.doc_type not in doc_types:
                continue
            if sims[i] <= 0.01:
                break
            out.append((c, float(sims[i])))
            if len(out) >= k:
                break
        return out
