from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import sys
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.rag import answer_question


HOST = "127.0.0.1"
PORT = 8000


HTML = """<!doctype html>
<html lang="tr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Yerel RAG Asistanı</title>
  <style>
    :root {
      color-scheme: light;
      --bg: #f6f8fb;
      --panel: #ffffff;
      --ink: #172033;
      --muted: #5d6b82;
      --line: #d9e0ea;
      --accent: #2563eb;
      --accent-dark: #1d4ed8;
      --ok: #0f766e;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: Segoe UI, system-ui, -apple-system, sans-serif;
      background: var(--bg);
      color: var(--ink);
    }
    .shell {
      min-height: 100vh;
      display: grid;
      grid-template-rows: auto 1fr;
    }
    header {
      border-bottom: 1px solid var(--line);
      background: var(--panel);
    }
    .bar {
      max-width: 1100px;
      margin: 0 auto;
      padding: 16px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
    }
    h1 {
      margin: 0;
      font-size: 20px;
      font-weight: 650;
    }
    .status {
      color: var(--ok);
      font-size: 14px;
      font-weight: 600;
    }
    main {
      max-width: 1100px;
      width: 100%;
      margin: 0 auto;
      padding: 24px 20px;
      display: grid;
      grid-template-columns: minmax(0, 1fr) 320px;
      gap: 18px;
    }
    .chat, .sources {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      min-width: 0;
    }
    .chat {
      display: grid;
      grid-template-rows: 1fr auto;
      min-height: 620px;
    }
    .messages {
      padding: 18px;
      overflow: auto;
    }
    .message {
      max-width: 760px;
      margin-bottom: 14px;
      padding: 12px 14px;
      border-radius: 8px;
      line-height: 1.45;
      white-space: pre-wrap;
    }
    .user {
      margin-left: auto;
      background: #e8f0ff;
      border: 1px solid #c7d8ff;
    }
    .assistant {
      background: #f8fafc;
      border: 1px solid var(--line);
    }
    form {
      border-top: 1px solid var(--line);
      padding: 14px;
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 10px;
    }
    input {
      width: 100%;
      padding: 12px 13px;
      border: 1px solid var(--line);
      border-radius: 8px;
      font: inherit;
      color: var(--ink);
    }
    button {
      border: 0;
      border-radius: 8px;
      background: var(--accent);
      color: #fff;
      padding: 0 18px;
      font: inherit;
      font-weight: 650;
      cursor: pointer;
    }
    button:hover { background: var(--accent-dark); }
    button:disabled { opacity: .55; cursor: wait; }
    .sources {
      padding: 16px;
    }
    .sources h2 {
      margin: 0 0 12px;
      font-size: 16px;
    }
    .source {
      border-top: 1px solid var(--line);
      padding: 12px 0;
    }
    .source:first-of-type { border-top: 0; }
    .source-title {
      font-weight: 650;
      margin-bottom: 4px;
    }
    .source-score {
      color: var(--muted);
      font-size: 13px;
    }
    .quick {
      display: grid;
      gap: 8px;
      margin-top: 12px;
    }
    .quick button {
      background: #eef2f7;
      color: var(--ink);
      border: 1px solid var(--line);
      padding: 9px 10px;
      text-align: left;
      font-weight: 500;
    }
    @media (max-width: 840px) {
      main { grid-template-columns: 1fr; }
      .chat { min-height: 520px; }
      form { grid-template-columns: 1fr; }
      button { min-height: 44px; }
    }
  </style>
</head>
<body>
  <div class="shell">
    <header>
      <div class="bar">
        <h1>Yerel RAG Asistanı</h1>
        <div class="status">Çevrimdışı yerel çalışma</div>
      </div>
    </header>
    <main>
      <section class="chat">
        <div class="messages" id="messages">
          <div class="message assistant">Foundry Local, RAG, SQLite veya proje iş akışı hakkında soru sor.</div>
        </div>
        <form id="form">
          <input id="question" autocomplete="off" placeholder="Bir soru yaz" />
          <button id="send" type="submit">Sor</button>
        </form>
      </section>
      <aside class="sources">
        <h2>Kaynaklar</h2>
        <div id="sources">Henüz kaynak yok.</div>
        <div class="quick">
          <button type="button" data-q="RAG nedir?">RAG nedir?</button>
          <button type="button" data-q="SQLite bu projede neden yararlıdır?">SQLite'ın rolü</button>
          <button type="button" data-q="Dokümanları değiştirdikten sonra ne yapmalıyım?">Doküman değişince</button>
          <button type="button" data-q="Fransa'nın başkenti nedir?">Eksik bilgi testi</button>
        </div>
      </aside>
    </main>
  </div>
  <script>
    const form = document.querySelector("#form");
    const input = document.querySelector("#question");
    const send = document.querySelector("#send");
    const messages = document.querySelector("#messages");
    const sources = document.querySelector("#sources");

    function addMessage(text, cls) {
      const div = document.createElement("div");
      div.className = `message ${cls}`;
      div.textContent = text;
      messages.appendChild(div);
      messages.scrollTop = messages.scrollHeight;
    }

    function renderSources(items) {
      if (!items.length) {
        sources.textContent = "Kaynak yok.";
        return;
      }
      sources.innerHTML = "";
      for (const item of items) {
        const div = document.createElement("div");
        div.className = "source";
        div.innerHTML = `<div class="source-title"></div><div class="source-score"></div>`;
        div.querySelector(".source-title").textContent = item.document_title;
        div.querySelector(".source-score").textContent = `Skor: ${item.score.toFixed(4)}`;
        sources.appendChild(div);
      }
    }

    async function ask(question) {
      addMessage(question, "user");
      send.disabled = true;
      input.disabled = true;
      try {
        const response = await fetch("/api/ask", {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({question})
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || "İstek başarısız oldu");
        addMessage(data.answer, "assistant");
        renderSources(data.sources || []);
      } catch (error) {
        addMessage(`Hata: ${error.message}`, "assistant");
      } finally {
        send.disabled = false;
        input.disabled = false;
        input.focus();
      }
    }

    form.addEventListener("submit", (event) => {
      event.preventDefault();
      const question = input.value.trim();
      if (!question) return;
      input.value = "";
      ask(question);
    });

    document.querySelectorAll("[data-q]").forEach((button) => {
      button.addEventListener("click", () => ask(button.dataset.q));
    });
  </script>
</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if urlparse(self.path).path != "/":
            self.send_error(404)
            return
        self._send(200, HTML.encode("utf-8"), "text/html; charset=utf-8")

    def do_POST(self) -> None:
        if urlparse(self.path).path != "/api/ask":
            self.send_error(404)
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            question = str(payload.get("question", "")).strip()
            if not question:
                raise ValueError("Soru gerekli.")
            result = answer_question(question)
            body = json.dumps(result, ensure_ascii=False).encode("utf-8")
            self._send(200, body, "application/json; charset=utf-8")
        except Exception as exc:
            body = json.dumps({"error": str(exc)}, ensure_ascii=False).encode("utf-8")
            self._send(400, body, "application/json; charset=utf-8")

    def log_message(self, format: str, *args) -> None:
        return

    def _send(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Aç: http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
