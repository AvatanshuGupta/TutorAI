from langchain_community.document_loaders import PyMuPDFLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter
splitter=RecursiveCharacterTextSplitter(
    chunk_size=1000,        
    chunk_overlap=200, 
)


def pdfDocs(file):
    loader = PyMuPDFLoader(file)
    docs = loader.load()
    docobj=splitter.split_documents(docs)
 
    return docobj,len(docobj)
