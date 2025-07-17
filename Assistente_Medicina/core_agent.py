from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

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

prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}"),
])

chain = prompt | llm

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