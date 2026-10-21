#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'reports'/'run-manifest.json').read_text())
lines=['# Baseline research report','',f"Dataset: `{manifest['dataset']}`  ",f"Seed: `{manifest['seed']}`  ",f"Rows after deduplication: `{manifest['rows']}`  ",f"Split sizes: `{manifest['split_sizes']}`",'', '| Model | Accuracy | Precision | Recall | Macro-F1 |','|---|---:|---:|---:|---:|']
for name, m in manifest['metrics'].items(): lines.append(f"| {name} | {m['accuracy']:.4f} | {m['precision']:.4f} | {m['recall']:.4f} | {m['macro_f1']:.4f} |")
lines += ['', '## Leakage and errors', f"Cross-split leakage findings: `{len(manifest['leakage'])}`.", 'Error rows are retained in `run-manifest.json` for inspection.', '', '## Scope', 'Implemented: CPU-only majority, keyword, and deterministic multinomial Naive Bayes baselines.', 'NOT_RUN: CNN, Transformer, GPU execution, fine-tuning, and real-world datasets.']
(root/'reports'/'baseline-report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(root/'reports'/'baseline-report.md')
