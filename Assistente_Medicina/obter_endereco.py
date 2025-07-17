import requests

import re

def formatar_cep(cep):
    return re.sub(r"[^0-9]", "", cep).zfill(8)[:5] + "-" + re.sub(r"[^0-9]", "", cep).zfill(8)[5:]

def obter_endereco(cep):
    url = f"https://viacep.com.br/ws/89227315/json/"
    resposta = requests.get(url)
    data = resposta.json()

    return data

print(obter_endereco(89227315))