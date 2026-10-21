# 第 11 章綜合專案契約：一週工作助理

## 唯一成果

讀者要交付一個可重播的週工作摘要包：

- `weekly-summary.md`
- `action-items.csv`
- `email-draft.md`
- `review-record.md`

## 資料來源

- `../sample-data/meeting-notes.md`
- `../sample-data/email-thread.md`
- `../sample-data/task-list.csv`
- `../sample-data/project-policy.md`

## 使用步驟

請從第一冊根目錄開始操作，不要直接修改 `companion/` 內的原始資料：

1. 複製 `companion/` 到自己的練習資料夾，例如 `my-weekly-assistant/`。
2. 先閱讀上列四個資料來源，並為每份資料保留來源編號：`E1`、`M1`、`T1`、`P1`。
3. 依序處理每份資料：移除不必要的敏感資料，整理事實、行動、期限、未知值和原文依據。
4. 把各份整理結果合併成一份 `action-items.csv`，每列保留 `source_id` 和 `status`。
5. 產生 `weekly-summary.md`、`email-draft.md` 和 `review-record.md`；可參考 `examples/` 的欄位和格式，但要在副本中建立自己的結果。
6. 逐項完成人工核對，將結果由 `draft` 改為 `checked`；最後對照 `replay-report.md` 檢查是否符合驗收條件。

建議的練習目錄如下：

```text
my-weekly-assistant/
├── input/                 # 複製後的四份來源資料
├── outputs/               # 你產生的四個交付檔案
└── review-record.md       # 人工核對紀錄
```

本專案不需要 API、Python 或外部自動化工具。可以使用一般文字編輯器、試算表和已批准的 AI 工具；若使用 AI，請只貼上去識別化副本，並把輸出先保存到 `outputs/`，不要直接寫回正式系統。

四個交付檔案的用途如下：

- `weekly-summary.md`：整理已確認的本週狀態、進行中事項和阻塞事項。
- `action-items.csv`：逐項列出事項、負責人、期限、狀態、來源和待確認欄位。
- `email-draft.md`：尚未寄出的內部電郵草稿。
- `review-record.md`：記錄核對人、日期、模板版本、修改內容和剩餘疑點。

`examples/` 是格式參考，不是要求照抄的完成答案。`replay-report.md` 是檢查資料契約和安全邊界的驗證紀錄，不是外部電郵或任務系統的執行證明。

## 狀態模型

- `draft`：AI 已產生，未完成人工核對。
- `checked`：已完成來源、數字、期限和安全核對。
- `approved`：有權限的人批准下一步。
- `executed`：實際操作已完成，並有系統讀回證據。

本書只要求讀者完成 `checked` 的摘要、行動清單和未寄出的電郵草稿；不得把示例資料送到真實外部系統，也不得把草稿標示為 `executed`。

## 驗收條件

- 所有任務均可追溯至 `source_id`。
- 未確認期限和負責人沒有被自行填補。
- 至少找出一個資料不足案例。
- 電郵是草稿，不是已寄出訊息。
- `review-record.md` 記錄核對人、時間、模板版本和剩餘疑點。
- 同一份輸入重新處理時，輸出欄位和狀態規則一致。
