# LABORATORIO 22 - EJERCICIO 5 y 6
# AUTORA: Velasquez Puma Brigitte Karolay

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os

HOST = "localhost"
PORT = 8001
INDEX_PATH = "static/index.html"

HTML_TEMPLATE = """<!doctype html>
<html>
<head><meta charset="utf-8"><title>Inicio</title></head>
<body>
  <h1>Servidor básico - Laboratorio 22</h1>
</body>
</html>
"""

class Handler(BaseHTTPRequestHandler):
    def _send_json(self, code, obj):
        b = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        if self.path == "/":
            os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)
            if not os.path.isfile(INDEX_PATH):
                with open(INDEX_PATH, "w", encoding="utf-8") as f:
                    f.write(HTML_TEMPLATE)
            with open(INDEX_PATH, "rb") as f:
                contenido = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(contenido)))
            self.end_headers()
            self.wfile.write(contenido)
            return

        if self.path == "/saludo":
            self._send_json(200, {"msg": "Hola"})
            return

        self.send_response(404)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"Ruta noo encontrada")

    def do_POST(self):
        if self.path == "/sumar":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode("utf-8") if length else ""
            try:
                data = json.loads(body)
                a = data.get("a")
                b = data.get("b")
                if not (isinstance(a, (int, float)) and isinstance(b, (int, float))):
                    raise ValueError("Campos 'a' y 'b' deben ser numericos.")
                self._send_json(200, {"suma": a + b})
            except json.JSONDecodeError:
                self._send_json(400, {"error": "JSON invalido"})
            except Exception as e:
                self._send_json(400, {"error": str(e)})
            return

        self.send_response(404)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"Ruta no encontrada")

if __name__ == "__main__":
    print(f"Servidor HTTP simple en http://{HOST}:{PORT}")
    server = HTTPServer((HOST, PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Servidor detenido.")
        server.server_close()
