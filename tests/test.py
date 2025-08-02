import requests

headers = {
  "Authorization": "Bearer Token123"
}

requisicao = requests.get("http://127.0.0.1:8000/auth/refresh", headers=headers)
print(requisicao)
print(requisicao.json)

# Em desenvolvimento