from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from pydantic import BaseModel,Field
from typing import Annotated
from langchain_core.prompts import PromptTemplate   
from langchain_core.output_parsers import PydanticOutputParser
import os
load_dotenv()


llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash",api_key=os.getenv("GOOGLE_API_KEY_ABH"))

class Quiz(BaseModel):
    question : Annotated[str,Field(title="Question",lt=100,gt=15,description="Question based on the given context it should be relevent meaningfull and straightforward and it should have 4 option out of which only one is correct leave the question blank if you cant make a question out of the provided question make strictly sure to not add anything on your own DONT HALLUCINATE ")]
    option1 : Annotated[str,Field(title="first option",lt=80,gt=15,description="this is the first option of the question")]
    option2 : Annotated[str,Field(title="second option",lt=80,gt=15,description="this is the second option of the question")]
    option3 : Annotated[str,Field(title="third option",lt=80,gt=15,description="this is the third option of the question")]
    option4 : Annotated[str,Field(title="fourth option",lt=80,gt=15,description="this is the fourth option of the question")]  




parser=PydanticOutputParser(pydantic_object=Quiz)

prompt_template = """
Based on the following context, generate a single multiple-choice question.

Requirements:
- The question must be relevant to the context.
- It must have exactly 4 options.
- Only one of the options should be correct.
- The question should be clear and straightforward.
- DO NOT add any content that is not supported by the context.
- Leave the question blank if a valid question cannot be created.
- You are also required to return the correct currect option 
- DO NOT HALLUCINATE
- The questions should be meaningfull and related to the context.
- The options should be meaningfull. 
- Don't return anything if you can't make valid question or option from the given context.
- The correct option should be the option number (NOT THE ACTUAL ANSWER), return these accordingly {{ "option1","option2","option3","option4" }}
    **USER CONTEXT:**
    ---
    {context}
    ---
Format your response as a JSON object following this schema:
{{
  "question": "<Your question here>",
  "option1": "<First option>",
  "option2": "<Second option>",
  "option3": "<Third option>",
  "option4": "<Fourth option>"
  "correctOption": "<Correct option>"
}}
"""
template=PromptTemplate(
    template=prompt_template,
    input_variables=['context'],
    partial_variables={'format':parser.get_format_instructions()}
    
)      
