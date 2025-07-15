from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from vector import buscar_contexto
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

template = """
    Você é um assistente de IA especialista em impressoras, capaz de ajudar com problemas técnicos, configuração e manutenção de impressoras.
    Você deve responder às perguntas de forma clara e concisa, fornecendo instruções passo a passo quando necessário.
    Quero que responda as perguntas, utilizando o contexto fornecido, onde contem manuais e boletins tecnicos de impressoras. Não traga resposta externa, apenas utilize o contexto.
    Se a pergunta não estiver relacionada a impressoras, informe que não é possível ajudar com esse assunto.
    Se a pergunta for muito vaga, peça mais detalhes ao usuário.

    Contexto: 
    {context}

    historico:
    {history}

    Pergunta: 
    {question}
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}")
])

llm = ChatOpenAI(
    temperature=0.3,
    model="gpt-4o-mini",
    api_key=api_key
)

chain = prompt | llm

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history"
)

def obter_resposta(pergunta: str, contexto: str, session_id="web-session"):
    resposta = chain_with_history.invoke(
        {
            "question": pergunta,
            "context": contexto
        },
        config={
            "configurable": {"session_id": session_id}
        }
    )

    return resposta