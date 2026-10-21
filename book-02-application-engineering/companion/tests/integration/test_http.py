import json
import threading
import urllib.request

from app.main import create_server


def test_healthz_and_ask_route(tmp_path):
    server = create_server("127.0.0.1", 0, data_path=tmp_path / "store.json", fixture_dir=__import__("pathlib").Path(__file__).parents[2] / "fixtures/documents")
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_port}"
    try:
        with urllib.request.urlopen(base + "/healthz") as response:
            assert response.status == 200
            assert json.load(response)["status"] == "ok"
        request = urllib.request.Request(base + "/ask", data=json.dumps({"query": "When is support open?", "tenant_id": "acme", "role": "support"}).encode(), headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(request) as response:
            body = json.load(response)
            assert response.status == 200
            assert body["answer"]
            assert "Support is open" in body["answer"]
            assert "Refunds are available" not in body["answer"]
    finally:
        server.shutdown()
        thread.join(timeout=2)


def test_server_from_environment(monkeypatch, tmp_path):
    monkeypatch.setenv("PORT", "0")
    monkeypatch.setenv("FIXTURE_DIR", str(__import__("pathlib").Path(__file__).parents[2] / "fixtures/documents"))
    monkeypatch.setenv("DATA_PATH", str(tmp_path / "store.json"))
    from app.main import create_server_from_environment

    server = create_server_from_environment()
    try:
        assert server.server_port != 8000
        assert len(server.agent.retriever.store.documents()) == 3
    finally:
        server.server_close()
