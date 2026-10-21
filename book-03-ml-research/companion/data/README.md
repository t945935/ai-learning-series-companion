# Data contract

`synthetic-messages.csv` is a deliberately small, fictional dataset. It has exactly `id,text,label` columns and labels `account`, `billing`, and `technical`. Duplicate IDs/text are removed by `src.data_contract`. No real personal data, external downloads, or network access are permitted.

The reproducible split uses seed `20261021`, stratified by label, with target proportions 60/20/20. Prepared JSON files are generated locally and are not committed as source data.
