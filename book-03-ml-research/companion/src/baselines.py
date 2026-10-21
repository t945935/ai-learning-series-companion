from collections import Counter
import math
import re

KEYWORDS = {
    "billing": ("invoice", "charge", "refund", "payment", "billing", "receipt"),
    "technical": ("error", "crash", "login", "password", "slow", "bug", "api"),
    "account": ("profile", "account", "address", "email", "close", "name"),
}


def majority_predict(train, rows):
    label = Counter(r["label"] for r in train).most_common(1)[0][0]
    return [label for _ in rows]


def keyword_predict(train, rows):
    majority = Counter(r["label"] for r in train).most_common(1)[0][0]
    predictions = []
    for row in rows:
        text = row["text"].lower()
        scores = {label: sum(bool(re.search(r"\b" + re.escape(word) + r"\b", text)) for word in words) for label, words in KEYWORDS.items()}
        best = max(scores, key=lambda label: (scores[label], label == majority))
        predictions.append(best if scores[best] else majority)
    return predictions


def multinomial_nb_predict(train, rows, alpha=1.0):
    """Deterministic sklearn-free bag-of-words alternative to logistic regression."""
    labels = sorted({r["label"] for r in train}); vocab = sorted({w for r in train for w in re.findall(r"[a-z]+", r["text"].lower())})
    counts = {label: Counter() for label in labels}; totals = Counter(); docs = Counter(r["label"] for r in train)
    for r in train:
        words = re.findall(r"[a-z]+", r["text"].lower()); counts[r["label"]].update(words); totals[r["label"]] += len(words)
    result=[]
    for r in rows:
        words = re.findall(r"[a-z]+", r["text"].lower()); scores={}
        for label in labels:
            score=math.log((docs[label]+alpha)/(len(train)+alpha*len(labels)))
            denom=totals[label]+alpha*len(vocab)
            score += sum(math.log((counts[label][w]+alpha)/denom) for w in words if w in vocab)
            scores[label]=score
        result.append(max(scores, key=scores.get))
    return result
