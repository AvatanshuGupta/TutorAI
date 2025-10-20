from langchain_huggingface import HuggingFaceEndpointEmbeddings
import os
from langchain_chroma import Chroma
model = "google/embeddinggemma-300m"
hf = HuggingFaceEndpointEmbeddings(
    model=model,
    task="feature-extraction",
    huggingfacehub_api_token=os.getenv("HUGGING_FACE_API"),
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_DIR = os.path.join(BASE_DIR, "vector_store_db")
COLLECTION_NAME = "uploadedPdf"

def embed_docs(file_doc):

    vector_store=Chroma(
        embedding_function=hf,
        persist_directory=CHROMA_DIR,
        collection_name=COLLECTION_NAME
    )

    vector_store.add_documents(file_doc)
    print(f"✅ Embedded {len(file_doc)} documents successfully")
    print("Available collections:", vector_store._client.list_collections())

def similar_embedding(query):
    vector_store=Chroma(
        embedding_function=hf,
        persist_directory=CHROMA_DIR,
        collection_name=COLLECTION_NAME
    )

    search_result=vector_store.similarity_search(
            query=query,
            k=3
            )
    print(f"🔍 Retrieved {len(search_result)} chunks for query '{query}'")

    return [res.page_content for res in search_result]

def check_count():
    # Initialize Chroma exactly as in your functions
    vector_store=Chroma(
        embedding_function=hf,
        persist_directory=CHROMA_DIR,
        collection_name=COLLECTION_NAME
    )
    print(f"Total documents loaded from disk: {vector_store._collection.count()}")

check_count()