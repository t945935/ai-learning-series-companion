import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from .agent import Agent
from .contracts import Principal
from .storage import KnowledgeStore


class Handler(BaseHTTPRequestHandler):
    server_version = "local-companion/0.1"

    def do_GET(self):
        if self.path == "/healthz":
            self._send(200, {"status": "ok"})
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/ask":
            self._send(404, {"error": "not found"})
            return
        try:
            data = json.loads(self.rfile.read(int(self.headers.get("Content-Length", "0"))))
            answer = self.server.agent.answer(data["query"], Principal(data["tenant_id"], data["role"]))
            self._send(200, {"answer": answer})
        except (KeyError, json.JSONDecodeError, TypeError) as exc:
            self._send(400, {"error": str(exc)})

    def _send(self, status, body):
        encoded = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, *_args):
        pass


def create_server(host="127.0.0.1", port=8000, data_path="store.json", fixture_dir=None):
    store = KnowledgeStore(data_path)
    if fixture_dir:
        for path in sorted(Path(fixture_dir).glob("*.md")):
            store.import_file(path)
    server = ThreadingHTTPServer((host, port), Handler)
    server.agent = Agent(store)
    return server


def create_server_from_environment():
    return create_server(
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", "8000")),
        data_path=os.getenv("DATA_PATH", "store.json"),
        fixture_dir=os.getenv("FIXTURE_DIR"),
    )


if __name__ == "__main__":
    server = create_server_from_environment()
    print(f"Serving local companion on http://{server.server_address[0]}:{server.server_port}")
    server.serve_forever()
