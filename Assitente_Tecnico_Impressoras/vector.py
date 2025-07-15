from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_community.document_loaders import UnstructuredPDFLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

def carregar_pdf(path):
    try:
        loader = UnstructuredPDFLoader(path, strategy="hi_res")
        docs = loader.load()
        if not docs or not docs[0].page_content.strip():
            raise ValueError("PDF vazio")
        return docs
    except:
        print(f"Fallback para PyPDFLoader: {path}")
        return PyPDFLoader(path).load()

def buscar_contexto(pergunta):
    docs = vector_store.similarity_search(pergunta, k=5)
    return "\n".join([doc.page_content for doc in docs])


db_location = "./chroma_langchain_db"
embeddings = OpenAIEmbeddings(api_key=api_key)

add_documents = not os.path.exists(db_location)

docs_path = [os.path.join("data", f) for f in os.listdir("data") if f.endswith(".pdf")]

documents = []
if add_documents:
    for path in docs_path:
        raw_docs = carregar_pdf(path)
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(raw_docs)
        for chunk in chunks:
            documents.append(Document(page_content=chunk.page_content, metadata=chunk.metadata))

    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=db_location
    )
else:
    vector_store = Chroma(
        persist_directory=db_location,
        embedding_function=embeddings
    )

