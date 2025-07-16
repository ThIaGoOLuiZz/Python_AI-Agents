from datasets import load_dataset
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os

def buscar_contexto(pergunta, k=5):
    docs = vector_store.similarity_search(pergunta, k=k)
    return "\n".join([doc.page_content for doc in docs])

embeddings = OllamaEmbeddings(model="mxbai-embed-large")
dataset = load_dataset("qiaojin/PubMedQA", "pqa_labeled")

db_location = "./chroma_db"

add_documents = not os.path.exists(db_location)

documents = []
if add_documents:

    for row in dataset["train"]:
        question = row["question"]
        context_chunk = row["context"]["contexts"]

        full_context = "\n".join(context_chunk)
        answer = row["long_answer"]

        doc = Document(
            page_content=f"Pergunta: {question}\nContexto: {full_context}\nResposta: {answer}",
            metadata = {"pubid": row["pubid"], "final_decision": row["final_decision"], "meshes": row["context"]["meshes"],"labels": row["context"]["labels"]}
        )

        documents.append(doc)

    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=db_location
    )

else:
    vector_store = Chroma(
        embedding_function=embeddings,
        persist_directory=db_location
    )