import streamlit as st
from core_chat import obter_resposta
from vector import buscar_contexto

st.set_page_config(page_title="Assistente Técnico de Impressoras")
st.title("Assistente Técnico")

if "messages" not in st.session_state:
    st.session_state.messages = []

pergunta = st.chat_input("Pergunte sobre problemas de impressoras...")

if pergunta:
    st.session_state.messages.append({"role": "user", "content": pergunta})

    with st.spinner("Analisando..."):
        contexto = buscar_contexto(pergunta)
        resposta_obj = obter_resposta(pergunta, contexto)

    st.session_state.messages.append({"role": "assistant", "content": resposta_obj.content})

# ✅ Exibe toda a conversa uma única vez:
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])