from langchain_text_splitters import RecursiveCharacterTextSplitter
from tutorAi.components.pdf_reader import pdfDocs
from langchain_core.prompts import PromptTemplate   
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel,Field
from typing import Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash",api_key=os.getenv("GOOGLE_API_KEY_VIK"))


class FlashcardModel(BaseModel):
    card : Annotated[str,Field(title="flash card",lt=150,gt=50,description="this is the flash card , it has to be concise and meaningfull explaining the concept or any information given in the context in simple words NOTE- LEAVE IT BLANK IF YOU CAN'T CREATE A MEANINGFULL FLASHCARD OUT OF THE CONTEXT")]



parser=PydanticOutputParser(pydantic_object=FlashcardModel)

temp_text="""
 You are an expert educational assistant specializing in concise knowledge summarization. Your task 
    is to analyze the provided USER CONTEXT and generate exactly one concise flashcard explaing the concept provided in context.

    **CONSTRAINTS AND RULES:**

    1.  **SOURCE ONLY:** Generate the content SOLELY from the text in the USER CONTEXT block.
    2.  **CONCISENESS:** The content must be more than 50 words and less than 150 words.
    3.  **BLANK RULE (CRITICAL):** If you cannot reliably and completely infer the required information from the provided context, you MUST return an empty string ('') for that specific field. Do not substitute, guess, or make up information.
    4.  **ONLY TEXT:** you are strictly instructed to provide only text, excluding any special character or labels just give simple text explaining the concept mention in context 

    **USER CONTEXT:**
    ---
    {context}
    ---
"""

template=PromptTemplate(
    template=temp_text,
    input_variables=['context'],
    partial_variables={'format':parser.get_format_instructions()}
    
)


class flash:
    def __init__(self,file):
        self.file=file
    def generate_flashcard(self):
        docs=pdfDocs(self.file)
        splitter=RecursiveCharacterTextSplitter(
            chunk_size=2000,        
            chunk_overlap=500, 
        )

        docobj=splitter.split_documents(docs)

        page_content=[]
        for doc in docobj:
            page_content.append(doc.page_content)

        card_list=[]
        for content in page_content:
            prompt=template.invoke({"context":content})
            card_list.append(llm.invoke(prompt))

        flash=[con.content for con in card_list]
        return flash
        