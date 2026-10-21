import random
from collections import defaultdict


def split_rows(rows, seed=20261021, proportions=(0.6, 0.2, 0.2)):
    rng = random.Random(seed)
    grouped = defaultdict(list)
    for row in rows: grouped[row["label"]].append(dict(row))
    output = {"train": [], "validation": [], "test": []}
    for label in sorted(grouped):
        items = grouped[label]; rng.shuffle(items)
        n = len(items); n_train = int(n * proportions[0]); n_val = int(n * proportions[1])
        if n >= 3: n_train = max(1, n_train); n_val = max(1, n_val)
        output["train"].extend(items[:n_train])
        output["validation"].extend(items[n_train:n_train+n_val])
        output["test"].extend(items[n_train+n_val:])
    for part in output.values(): part.sort(key=lambda r: r["id"])
    return output
