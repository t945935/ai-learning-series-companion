# 第三冊 CPU 研究 companion

這是第三冊的唯一核心重播路線：離線、CPU、標準庫、固定 seed、小型合成客服訊息資料。它會驗證資料契約、去重、固定分層切分，執行 majority、keyword 和 deterministic Multinomial Naive Bayes 三個 baseline，計算 Accuracy／Precision／Recall／Macro-F1，檢查跨切分洩漏，保存錯誤並產生研究報告。

## 從乾淨環境開始

以下命令由系列根目錄（包含 `03-ai-ml-research/` 的目錄）執行：

```bash
cd 03-ai-ml-research/companion
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
python scripts/run_baseline.py
python scripts/build_report.py
```

Windows PowerShell：

```powershell
cd 03-ai-ml-research\companion
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest -q
python scripts/run_baseline.py
python scripts/build_report.py
```

結果檔案：

- `reports/run-manifest.json`：資料、seed、切分、指標、錯誤和狀態
- `reports/baseline-report.md`：由 manifest 產生的報告

這條核心路線不需要網路、GPU、模型下載或真實個人資料。第三冊根目錄的 `environment-guide.md` 說明 NumPy／Pandas／scikit-learn 和 PyTorch／Transformers 的延伸環境；那些依賴不會自動成為核心驗收條件。

## 第 14 章對接

第 14 章的核心交付物就是本 companion 產生的兩份報告。不要把章內的 TF-IDF／attention 示範數字填入這份 manifest；若執行延伸模型，請使用另一個 run 目錄和另一份資料／環境紀錄。

## Scope status

- DONE: contract validation, deduplication, fixed seed split, majority baseline, keyword baseline, deterministic sklearn-free multinomial Naive Bayes, metrics, leakage checks, error analysis, manifest, report generation.
- NOT_RUN extension: CNN, Transformer, GPU, fine-tuning, real-world datasets, and external model downloads.

See `data/README.md`, `data/manifests/dataset-v1.json`, and `reports/README.md` for contracts.
