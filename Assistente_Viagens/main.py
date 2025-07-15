import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

load_dotenv()

template = """
Você é um assistente de IA especializado em viagens, auxiliando o usuario a planejar viajens, dando sugestões de destinos, roteiros e dicas práticas.
A primeira coisa que você deve fazer é perguntar para onde o usuario vai, com quantas pessoas e por quantos dias.

histórico de conversa:
{history}

Entrada do usuário:
{input}
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

llm = ChatOpenAI(
    temperature=0.7,
    model="gpt-4o-mini"
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
    input_messages_key="input",
    history_messages_key="history"
)

def iniciar_assistente():
    print("Bem-vindo ao Assistente de Viagens!")
    while True:
        pergunta_usuario = input("Você: ")

        if pergunta_usuario.lower() in ["sair", "exit", "quit"]:
            print("Assistente: Até logo!")
            break

        resposta = chain_with_history.invoke(
            {"input": pergunta_usuario},
            config={"configurable": {"session_id": "user123"}}
        )

        print("Assistente:", resposta.content)

if __name__ == "__main__":
    iniciar_assistente()