from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import re


llm = OllamaLLM(model="llama3.2", temperature=0.1)

template = """
Você é um desenvolvedor Python especialista em automações RPA usando Selenium 4+.

Sua tarefa é gerar apenas um trecho de código Python completo e funcional que adicione exatamente uma nova etapa de automação, baseada em:

- Código Python atual (se existir),
- Descrição da nova etapa,
- HTML da página atual (somente para referência dos seletores).

Regras absolutamente obrigatórias:

- NÃO gere nenhuma etapa que não esteja na descrição da nova etapa.
- NÃO use 'print' em nenhuma circunstância, nem mensagens, nem logs.
- NÃO inclua comentários, explicações, ou marcação Markdown no código.
- Use apenas métodos modernos do Selenium 4+ (por exemplo, `driver.find_element(By.ID, "id")`).
- Sempre atualize a variável `body` no final da etapa com:
  
  `body = BeautifulSoup(driver.page_source, "html.parser").body`
  
- Se o código estiver vazio, inicie o driver, carregue a URL e atualize `body`.
- NÃO repita o código já existente; apenas complemente com a nova etapa.
- O código gerado deve conter apenas as linhas necessárias para a nova etapa e a atualização final do `body`.
- Se precisar armazenar valores para uso futuro, use variáveis, mas nunca imprima ou exiba.
- Retorne somente código Python limpo, nada mais.

Adicione apenas uma linha para a nova etapa e a body atualizada no final. Não adicione nada mais

Entradas:

Código atual:
{code}

Nova etapa:
{etapa}

HTML da página (para referência dos seletores):
{body}
"""

prompt = ChatPromptTemplate.from_template(template)

chain = prompt | llm

etapas = []
contador_etapas = 1
while True:
    etapa = input(f"Descreva a etapa {contador_etapas} (Para sair digite 'q'): ")
    if etapa == 'q':
        break
    etapas.append(etapa)



url = "https://suporte.website.com.br/areacliente/login"

codigo = f"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--log-level=3")  # Minimiza logs do Chrome (0-3; 3 = ERRORS only)
options.add_argument("--disable-logging")
options.add_argument("--disable-infobars")
options.add_argument("--disable-notifications")

driver = webdriver.Chrome(options=options)
driver.get("{url}")
driver.page_source

body = BeautifulSoup(driver.page_source, "html.parser").body
"""

print("Obtendo codigo...")
retorno = {}
for etapa in etapas:
    exec(codigo, retorno)
    body = retorno["body"]

    result = chain.invoke(
        {
            "code": codigo,
            "etapa": etapa,
            "body": body
        }
    )

    codigo = re.sub(r"```(?:python)?\n(.*?)```", r"\1", result, flags=re.DOTALL) 

print(codigo)