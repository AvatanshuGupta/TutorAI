from langchain_community.document_loaders import PyMuPDFLoader



def pdfDocs(file):
    loader = PyMuPDFLoader(file)
    docs = loader.load()
    return docs,len(docs)
