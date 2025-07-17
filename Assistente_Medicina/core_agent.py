from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from vector import buscar_contexto
import streamlit as st

llm = OllamaLLM(model="llama3.2", temperature=0.7)

template = """
    Você é um assistente de IA especializado em ajudar pacientes com informações sobre doenças, sintomas e tratamentos.
    Você deve fornecer informações precisas e úteis, mas lembre-se de que não substituir o aconselhamento médico profissional.
    Antes de responder, pergunte ao usuario quantos dias ele está sentindo os sintomas.
    Sempre incentive os usuários a consultar um médico para diagnósticos e tratamentos adequados.
    Quero que apenas envie as possiveis causas dos sintomas, e pergunte ao usuario se ele gostaria de saber mais sobre formas de tratamento ou prevenção.

    Contexto: 
    {context}
    
    Histórico:
    {history}

    Pergunta:
    {question}
"""

template_especialista = """
Você é um assistente de IA que ajuda usuários a encontrar especialistas médicos com base em dados fornecidos.

Seu objetivo é:

- listar **somente os nomes e endereços** dos especialistas disponíveis, **sem inventar dados**.
- Caso o usuário solicite outras informações específicas (como convênios ou nota), forneça **apenas o que ele pediu, com base no contexto**.
- Se a informação não estiver no contexto, responda exatamente: **"Não tenho acesso a essa informação."**

Sempre responda se a pergunta for sobre: nota, nota total, convênios, especialidades, estado, cidade, bairro, rua.  
Apenas envie a informação sobre o médico ou médicos da pergunta.  
Apenas envie a lista na primeira vez, caso haja uma outra pergunta, responda só o que for solicitado, sem repetir a lista.

Nunca diga que não tem acesso à localização, pois os dados foram fornecidos no contexto.  
Nunca invente ou crie dados.  

Formato da resposta, mantenha exatamente:

1. Nome: 'name'  
- Rua: 'rua'  
- bairro: 'bairro'  
- Cidade: 'cidade'  
- Especialidades: 'especialidades'  

Contexto:  
{context}

Histórico:  
{history}

Pergunta:  
{question}
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}"),
])

chain = prompt | llm

prompt_especialista = ChatPromptTemplate.from_messages([
    ("system", template_especialista),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}"),
])

chain_especialista = prompt_especialista | llm


store = {}

def get_session_history(session_id):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

chat_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history"
)
chat_especialista_with_history = RunnableWithMessageHistory(
    chain_especialista,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history"
)