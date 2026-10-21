#!/usr/bin/env python3
import json, sys
from datetime import datetime, timezone
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.data_contract import load_csv
from src.split import split_rows
from src.baselines import majority_predict, keyword_predict, multinomial_nb_predict
from src.evaluate import classification_metrics
from src.error_analysis import detect_leakage, find_errors

root=Path(__file__).resolve().parents[1]
rows=load_csv(root/'data/raw/synthetic-messages.csv'); splits=split_rows(rows)
labels=sorted({r['label'] for r in rows}); results={}; errors={}
for name, fn in [('majority', majority_predict), ('keyword', keyword_predict), ('multinomial_nb', multinomial_nb_predict)]:
    pred=fn(splits['train'], splits['test']); true=[r['label'] for r in splits['test']]
    results[name]=classification_metrics(true, pred, labels); errors[name]=find_errors(splits['test'], pred)
manifest={'dataset':'synthetic-messages-v1','seed':20261021,'rows':len(rows),'split_sizes':{k:len(v) for k,v in splits.items()},'leakage':detect_leakage(splits),'metrics':results,'errors':errors,'created_utc':datetime.now(timezone.utc).isoformat(),'status':'CPU_REPRODUCED'}
out=root/'reports'/'run-manifest.json'; out.write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps(manifest,indent=2))
