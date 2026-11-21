"""Lightweight OpenAI-compatible proxy for Vertex AI Gemma 4 MaaS (Global Endpoint)
Translates OpenAI chat completion requests to google.genai Vertex AI Client.
Zero extra dependencies - runs on Python standard library + google-genai.
"""

import json
import os
import sys
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

try:
    from google import genai
except ImportError:
    print("Error: google-genai package required. Install with: pip install google-genai", file=sys.stderr)

PROJECT_ID = os.environ.get("VERTEXAI_PROJECT") or os.environ.get("GCP_PROJECT") or "lab-ai-972593"
LOCATION = os.environ.get("VERTEXAI_LOCATION") or "global"
DEFAULT_MODEL = os.environ.get("GEMMA_MODEL") or "gemma-4-26b-a4b-it-maas"

# Initialize Client
client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)


class ThreadingServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True


class ProxyHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Keep logs clean
        sys.stderr.write(f"[{time.strftime('%X')}] {format % args}\n")

    def do_GET(self):
        if self.path in ("/health", "/v1/health", "/"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status":"ok","model":"gemma-4-26b-a4b-it-maas"}')
        elif self.path in ("/models", "/v1/models"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            data = {
                "object": "list",
                "data": [
                    {"id": "gemma-4-26b", "object": "model", "owned_by": "google"},
                    {"id": "gemini-3.8-flash", "object": "model", "owned_by": "google"},
                    {"id": "claude-opus-5-5", "object": "model", "owned_by": "google"},
                    {"id": "gemini-4-argon", "object": "model", "owned_by": "google"},
                ]
            }
            self.wfile.write(json.dumps(data).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path not in ("/chat/completions", "/v1/chat/completions"):
            self.send_response(404)
            self.end_headers()
            return

        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)

        try:
            req = json.loads(post_data.decode("utf-8"))
            messages = req.get("messages", [])
            stream = req.get("stream", False)

            # Build contents for genai Client
            contents = []
            system_instruction = None

            for msg in messages:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                if role == "system":
                    system_instruction = content
                elif role in ("user", "assistant"):
                    mapped_role = "model" if role == "assistant" else "user"
                    contents.append({"role": mapped_role, "parts": [{"text": str(content)}]})

            if not contents:
                contents = [{"role": "user", "parts": [{"text": "Hello"}]}]

            config = {}
            if system_instruction:
                config["system_instruction"] = system_instruction
            if "temperature" in req:
                config["temperature"] = req["temperature"]
            if "max_tokens" in req:
                config["max_output_tokens"] = req["max_tokens"]

            res = client.models.generate_content(
                model=DEFAULT_MODEL,
                contents=contents,
                config=config if config else None
            )

            response_text = res.text or ""

            if stream:
                # SSE streaming format
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream")
                self.send_header("Cache-Control", "no-cache")
                self.end_headers()

                chunk = {
                    "id": f"chatcmpl-{int(time.time())}",
                    "object": "chat.completion.chunk",
                    "created": int(time.time()),
                    "model": "gemma-4-26b",
                    "choices": [{
                        "index": 0,
                        "delta": {"role": "assistant", "content": response_text},
                        "finish_reason": "stop"
                    }]
                }
                self.wfile.write(f"data: {json.dumps(chunk)}\n\n".encode("utf-8"))
                self.wfile.write(b"data: [DONE]\n\n")
            else:
                resp_json = {
                    "id": f"chatcmpl-{int(time.time())}",
                    "object": "chat.completion",
                    "created": int(time.time()),
                    "model": "gemma-4-26b",
                    "choices": [{
                        "index": 0,
                        "message": {"role": "assistant", "content": response_text},
                        "finish_reason": "stop"
                    }],
                    "usage": {
                        "prompt_tokens": len(str(messages)) // 4,
                        "completion_tokens": len(response_text) // 4,
                        "total_tokens": (len(str(messages)) + len(response_text)) // 4
                    }
                }
                body = json.dumps(resp_json).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

        except Exception as e:
            sys.stderr.write(f"Proxy error: {e}\n")
            err_body = json.dumps({"error": {"message": str(e), "type": "proxy_error"}}).encode("utf-8")
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(err_body)))
            self.end_headers()
            self.wfile.write(err_body)


def run_server(port=4000):
    server = ThreadingServer(("0.0.0.0", port), ProxyHandler)
    print(f"Vertex AI Gemma 4 Proxy running on http://0.0.0.0:{port} (Model: {DEFAULT_MODEL}, Region: {LOCATION})")
    server.serve_forever()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 4000
    run_server(port)
