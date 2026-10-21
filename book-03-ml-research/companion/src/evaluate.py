from collections import Counter


def classification_metrics(y_true, y_pred, labels):
    if not y_true: return {"accuracy": 0.0, "precision": 0.0, "recall": 0.0, "macro_f1": 0.0}
    accuracy = sum(a == b for a,b in zip(y_true,y_pred))/len(y_true)
    ps=[]; rs=[]; fs=[]
    for label in labels:
        tp=sum(a==label and b==label for a,b in zip(y_true,y_pred)); fp=sum(a!=label and b==label for a,b in zip(y_true,y_pred)); fn=sum(a==label and b!=label for a,b in zip(y_true,y_pred))
        p=tp/(tp+fp) if tp+fp else 0.0; r=tp/(tp+fn) if tp+fn else 0.0; f=2*p*r/(p+r) if p+r else 0.0
        ps.append(p); rs.append(r); fs.append(f)
    return {"accuracy": accuracy, "precision": sum(ps)/len(ps), "recall": sum(rs)/len(rs), "macro_f1": sum(fs)/len(fs)}
