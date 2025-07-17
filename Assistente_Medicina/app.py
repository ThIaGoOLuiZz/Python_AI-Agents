import streamlit as st
from core_agent import chat_with_history
from vector import buscar_contexto
from scrapping_especialistas import retornar_json
from obter_endereco import obter_endereco
import json
import re

st.set_page_config(page_title="Assistente Médico", page_icon="🩺")
st.title("Assistente Médico com IA")

if "session_id" not in st.session_state:
    st.session_state.session_id = "sessao_default"

if "messages_sintomas" not in st.session_state:
    st.session_state.messages_sintomas = []

if "messages_especialistas" not in st.session_state:
    st.session_state.messages_especialistas = []

modo = st.radio("Escolha o tipo de assistência:", ["🩺 Sintomas", "👨‍⚕️ Especialistas"])

if modo == "🩺 Sintomas":
    for msg in st.session_state.messages_sintomas:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Descreva seus sintomas aqui...")

    if user_input:
        st.session_state.messages_sintomas.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        contexto = buscar_contexto(user_input)

        resposta = chat_with_history.invoke(
            {
                "question": user_input,
                "context": contexto,
            },
            config={"configurable": {"session_id": st.session_state.session_id + "_sintomas"}}
        )

        st.session_state.messages_sintomas.append({"role": "assistant", "content": resposta})
        with st.chat_message("assistant"):
            st.markdown(resposta)

if modo == "👨‍⚕️ Especialistas":
    especialidade = st.selectbox("Escolha a especialidade:", [
        "pediatras", "cardiologistas", "dermatologistas", "neurologistas", "ginecologistas"
    ])

    cep = st.text_input("Digite seu CEP (formato 00000-000)", max_chars=9, placeholder="00000-000")

    quantidade = st.slider("Quantidade de especialistas a retornar", min_value=1, max_value=10, value=5)

    botao_consultar = st.button("Consultar Especialistas")

    if botao_consultar:
        cep_formatado = re.sub(r"[^0-9]", "", cep)
        if len(cep_formatado) != 8:
            st.warning("CEP inválido. Use o formato 00000-000.")
        else:
            cep_formatado = cep_formatado[:5] + '-' + cep_formatado[5:]

            try:
                endereco = obter_endereco(cep_formatado)
                cidade = endereco.get("localidade", "").lower()
                estado = endereco.get("uf", "").lower()
                st.info(f"🔍 Buscando especialistas em {especialidade} na região de {cidade.upper()} - {estado.upper()}...")


                dados_especialistas = retornar_json(especialidade, cidade, estado)

                if dados_especialistas:
                    st.success(f"Especialistas encontrados.")

                    for i,especialista in enumerate(dados_especialistas[:quantidade]):
                        st.markdown(f"""
                        {i + 1}. **Nome:** {especialista.get('name', 'Não informado')}  
                        - Rua: {especialista.get('rua', 'Não informado')}  
                        - Bairro: {especialista.get('bairro', 'Não informado')}  
                        - Cidade: {especialista.get('cidade', 'Não informado')}  
                        - Estado: {especialista.get('estado', 'Não informado')}  
                        - Especialidades: {', '.join(especialista.get('especialidades', [])) if especialista.get('especialidades') else 'Não informado'}
                        - Convênios: {', '.join(especialista.get('convenios', [])) if especialista.get('convenios') else 'Não informado'}
                        - Nota Total: {especialista.get('nota_total', 'Não informado')}  
                        """)

                else:
                    st.warning("Nenhum especialista encontrado para a região e especialidade informada.")

            except Exception as e:
                st.error(f"Ocorreu um erro ao buscar os especialistas: {e}")