# Book 2 companion: local mock AI knowledge workbench core

This is a small, replayable local mock core slice for teaching. It is not the complete production workbench promised by a generic architecture diagram. The implemented HTTP surface is intentionally small:

- `GET /healthz`
- `POST /ask`

The local core uses only the Python standard library at runtime:

- deterministic SHA-256 `source_id` document fixtures;
- metadata-aware tenant/role filtering;
- token-overlap lexical search (not embeddings);
- explicit no-evidence refusal;
- a typed `create_ticket` tool with approval, idempotency, and audit events;
- bounded agent execution and safety stop.

`contracts.md` also describes target interfaces for a future expanded workbench. Those routes are contract material unless a corresponding implementation and HTTP test is listed below.

## Run

```bash
cd 02-ai-application-engineering/companion
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e .
pytest -q
PORT=18000 FIXTURE_DIR=fixtures/documents DATA_PATH=/tmp/book2-store.json python -m app.main
```

Windows PowerShell：

```powershell
$env:PORT="18000"
$env:FIXTURE_DIR="fixtures/documents"
$env:DATA_PATH="$pwd\book2-store.json"
python -m app.main
```

Then post JSON to the port selected above:

```json
{"query":"When is support open?","tenant_id":"acme","role":"support"}
```

Use `GET /healthz` first. The fixture directory must be supplied; otherwise the in-memory store contains no documents and `/ask` should refuse rather than invent an answer.

## Explicit limits

The companion is a mock/local implementation. It does **not** call an external network, real LLM, vector database, ticketing system, or cloud deployment. Search is lexical and the agent formats retrieved local evidence; it is not a model-generated answer. `KnowledgeStore` is in-memory for the process (the path is reserved for a future persistence exercise). No authentication is provided; tenant and role are request fields for demonstration and must not be treated as production security.

`evals/rag-golden.jsonl` contains deterministic scenarios suitable for replay.
