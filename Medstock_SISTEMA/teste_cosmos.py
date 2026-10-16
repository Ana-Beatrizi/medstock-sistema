
import os
import requests

token = os.getenv("COSMOS_TOKEN", "").strip()

# Substitua pelo User-Agent exato fornecido
# no painel da sua conta Cosmos.
user_agent = "COLE_AQUI_SEU_USER_AGENT_OFICIAL"

if not token:
    print("ERRO: token não foi carregado.")
    raise SystemExit(1)

url = "https://api.cosmos.bluesoft.com.br/gtins/7891910000197.json"

headers = {
    "X-Cosmos-Token": token,
    "User-Agent": user_agent,
    "Content-Type": "application/json"
}

try:
    resposta = requests.get(
        url,
        headers=headers,
        timeout=15
    )

    print("Status HTTP:", resposta.status_code)

    if resposta.status_code == 200:
        dados = resposta.json()
        print("Conexão com Cosmos: OK")
        print("Produto:", dados.get("description"))
        print("Marca:", (dados.get("brand") or {}).get("name"))
        print("GTIN:", dados.get("gtin"))

    elif resposta.status_code in (401, 403):
        print("Falha de autenticação ou acesso.")
        print("Confira o token e o User-Agent.")

    elif resposta.status_code == 404:
        print("Produto não encontrado nesse endpoint.")

    elif resposta.status_code == 429:
        print("Limite de consultas da API atingido.")

    else:
        print("Resposta:", resposta.text[:500])

except requests.RequestException as erro:
    print("Erro de conexão:", erro)
