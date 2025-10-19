from langchain_text_splitters import RecursiveCharacterTextSplitter
splitter=RecursiveCharacterTextSplitter(
    chunk_size=2000,        
    chunk_overlap=500, 
)