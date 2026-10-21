# Baseline research report

Dataset: `synthetic-messages-v1`  
Seed: `20261021`  
Rows after deduplication: `36`  
Split sizes: `{'train': 21, 'validation': 6, 'test': 9}`

| Model | Accuracy | Precision | Recall | Macro-F1 |
|---|---:|---:|---:|---:|
| majority | 0.3333 | 0.1111 | 0.3333 | 0.1667 |
| keyword | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| multinomial_nb | 0.6667 | 0.8333 | 0.6667 | 0.6556 |

## Leakage and errors
Cross-split leakage findings: `0`.
Error rows are retained in `run-manifest.json` for inspection.

## Scope
Implemented: CPU-only majority, keyword, and deterministic multinomial Naive Bayes baselines.
NOT_RUN: CNN, Transformer, GPU execution, fine-tuning, and real-world datasets.
