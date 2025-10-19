from langchain_community.document_loaders import PyMuPDFLoader

def pdfReader(file):
    loader = PyMuPDFLoader(file)
    docs = loader.load()
    content=[doc.page_content for doc in docs]
    return content,len(docs)

def pdfDocs(file):
    loader = PyMuPDFLoader(file)
    docs = loader.load()
    return docs
