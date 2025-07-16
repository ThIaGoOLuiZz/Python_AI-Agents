import streamlit as st
from core_agent import chat_with_history
from vector import buscar_contexto

st.set_page_config(page_title="Assistente Médico", page_icon="🩺")
st.title("Assistente Médico com IA")

if "session_id" not in st.session_state:
    st.session_state.session_id = "sessao_default"

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Descreva seus sintomas aqui...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    contexto = buscar_contexto(user_input)

    resposta = chat_with_history.invoke(
        {
            "question": user_input,
            "context": contexto,
        },
        config={"configurable": {"session_id": st.session_state.session_id}}
    )

    st.session_state.messages.append({"role": "assistant", "content": resposta})
    with st.chat_message("assistant"):
        st.markdown(resposta)