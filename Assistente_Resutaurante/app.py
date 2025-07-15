import streamlit as st
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever

model = OllamaLLM(model="llama3.2")

template = """
You are an expert inanswering questions about a pizza restaurant

Here are some relevant reviews: {reviews}

Here is the question to answer: {question}
"""

prompt = ChatPromptTemplate.from_template(template)

chain = prompt | model

st.set_page_config(page_title="PizzaBot", layout="centered")
st.title("Ask anything about the place!")

question = st.text_input("Enter your question:")

if question:
    with st.spinner("Retrieving reviews and generating response..."):
        reviews = retriever.invoke(question)
        result = chain.invoke({"reviews": reviews, "question": question})

    st.markdown("## Assistant:")
    st.write(result)