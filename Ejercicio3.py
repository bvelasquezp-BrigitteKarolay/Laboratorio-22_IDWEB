# LABORATORIO 22 - EJERCICIO 3
# AUTORA: Velasquez Puma Brigitte Karolay


import urllib.request
import json
import ssl

def consultar_httpbin():
    url = "https://httpbin.org/get"
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={"User-Agent": "python-urllib/3"})
    with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
        body = resp.read().decode("utf-8")
    data = json.loads(body)


    print("IP (origin):", data.get("origin"))
    print("\nHeaders (server recibió):")
    headers = data.get("headers", {})
    for k, v in headers.items():
        print(f"  {k}: {v}")
    print("\nArgs (query params):", data.get("args"))

if __name__ == "__main__":
    try:
        consultar_httpbin()
    except Exception as e:
        print("Error al consultar httpbin:", e)
