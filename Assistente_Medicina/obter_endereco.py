import requests

import re

def formatar_cep(cep):
    return re.sub(r"[^0-9]", "", cep).zfill(8)[:5] + "-" + re.sub(r"[^0-9]", "", cep).zfill(8)[5:]

def obter_endereco(cep):
    url = f"https://cdn.apicep.com/file/apicep/{cep}.json"
    resposta = requests.get(url)
    data = resposta.json()

    return data