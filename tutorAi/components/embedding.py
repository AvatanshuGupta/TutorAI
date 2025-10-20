from langchain_huggingface import HuggingFaceEndpointEmbeddings
import os
from langchain_chroma import Chroma
model = "google/embeddinggemma-300m"
hf = HuggingFaceEndpointEmbeddings(
    model=model,
    task="feature-extraction",
    huggingfacehub_api_token=os.getenv("HUGGING_FACE_API"),
)

def embed_docs(file_doc):

    vector_store=Chroma(
        embedding_function=hf,
        persist_directory="./vector_store_db",
        collection_name="uploadedPdf"
    )

    vector_store.add_documents(file_doc)
    print(vector_store._client.list_collections())

def similar_embedding(query):
    vector_store=Chroma(
        embedding_function=hf,
        persist_directory="./vector_store_db",
        collection_name="uploadedPdf"
    )

    search_result=vector_store.similarity_search(
            query=query,
            k=3
            )
    return [res.page_content for res in search_result]

