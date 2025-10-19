from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash",api_key=os.getenv("GOOGLE_API_KEY_ABH"))