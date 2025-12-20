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

    print("IP:", data.get("origin"))
    print("Headers:")
    for k, v in data.get("headers", {}).items():
        print(k, ":", v)
    print("Args:", data.get("args"))

if __name__ == "__main__":
    consultar_httpbin()
