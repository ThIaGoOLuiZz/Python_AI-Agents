import requests
from lxml import html

def obter_links(especialidade, cidade, estado):

    url=f"https://www.boaconsulta.com/especialistas/{especialidade}/{cidade}-{estado}/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9",
    }
    page = requests.get(url=url, headers=headers)
    tree = html.fromstring(page.content)
    list = tree.xpath("//a[@id='search-item-name-profile-link']/@href")
    return list

def obter_info_especialista(link):
    url = "https://www.boaconsulta.com" + link
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9",
    }

    page = requests.get(url=url, headers=headers)
    tree = html.fromstring(page.content)

    name = tree.xpath("//h1[@itemprop='name']/text()")
    rua = tree.xpath("//span[@itemprop='streetAddress']/text()")
    bairro = tree.xpath("//h3[contains(@class,'speakable-locations-name')]/text()")
    cidade = tree.xpath("//span[@itemprop='addressLocality']/text()")
    estado = tree.xpath("//span[@itemprop='addressRegion']/text()")
    especialidades = tree.xpath("//h2[@class='speakable-locations-specialties']//button/text()")
    convenios = tree.xpath("//a[contains(@href, 'agendamento/convenio')]/text()")
    nota_total = tree.xpath("//div[contains(@class,'speakable-locations-reviews')]//p[contains(@class,'text-4xl')]/text()")
    
    valores = {
        "name": name[0].strip() if name else "",
        "rua": rua[0].strip() if rua else "",
        "bairro": bairro[0].strip() if bairro else "",
        "cidade": cidade[0].strip() if cidade else "",
        "estado": estado[0].strip() if estado else "",
        "especialidades": [i.strip() for i in especialidades] if especialidades else [],
        "convenios": [i.strip() for i in convenios] if convenios else [],
        "nota_total": nota_total[0].strip() if nota_total else ""
    }

    return valores

def retornar_json(especialista, cidade, estado):
    links = obter_links(especialista,cidade,estado)

    lista = []
    for i in links:
        retorno = obter_info_especialista(i)
        lista.append(retorno)

    return lista