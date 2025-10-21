from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
from tutorAi.components.pdf_reader import pdfDocs
from tutorAi.components.quiz import QuizBuilder
from tutorAi import settings
from tutorAi.components.flashcard import flash
from tutorAi.components.embedding import embed_docs,similar_embedding
from tutorAi.components.chat import should_retrieve
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from django.http import JsonResponse,StreamingHttpResponse
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
import os
import re
load_dotenv()

MAX_PDF_PAGE=30

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",api_key=os.getenv("GOOGLE_API_KEY_AVG"))
llm2 = ChatGoogleGenerativeAI(model="gemma-3-27b",api_key=os.getenv("GOOGLE_API_KEY_LUC"))


chat_template = ChatPromptTemplate.from_messages([
    ("system", 
     "You are a helpful AI study assistant. "
     "If I provide you with context, use it to answer the question accurately. "
     "If no context is given, answer based only on your own knowledge. "
     "Always respond conversationally and clearly."
    ),
    MessagesPlaceholder(variable_name="chat_hist"),
    ("human", 
     "Context (if any): {context}\n\n"
     "Question: {query}"
    )
])




def upload_pdf(request):
    if request.method== "POST" and request.FILES.get("pdf"):
        pdf_file=request.FILES['pdf']
        fs=FileSystemStorage(location='media/temp')
        filename = fs.save(pdf_file.name, pdf_file)
        

        file_path = os.path.join(settings.MEDIA_ROOT, 'temp', filename)
        
        try:
            
            docobj,page_count=pdfDocs(file_path)
            if page_count>MAX_PDF_PAGE:
                fs.delete(filename)
                return render(request,'home.html',{
                    "error_message": f"PDF is too large. Max pages allowed is {MAX_PDF_PAGE}, but your file has {page_count} pages."
                })

            try:    
                
                embed_docs(docobj) 
                
                
            except Exception as embed_e:
                print(f"Embedding failed due to: {embed_e}")

            
            request.session.flush()
            request.session["pdf_path"] = file_path
            request.session["pdf_name"] = pdf_file.name
            
            return redirect('dashboard')
            
        except Exception as e:
            fs.delete(filename)
            return render(request, "home.html", {
                "error_message": "An error occurred during file processing"
            })
        
    return render(request, "home.html")


def chat_with_pdf(request):
    if request.method != 'POST' or not request.body:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    try:
        data = json.loads(request.body)
        user_query = data.get('query', '')
            
        if not user_query:
                return JsonResponse({'error': 'No query provided'}, status=400)
        chat_hist_data = request.session.get('chat_hist', [])

        chat_hist = [
                HumanMessage(content=msg['content']) if msg['type'] == 'human' 
                else AIMessage(content=msg['content'])
                for msg in chat_hist_data
            ]
        
        chat_hist = [
                HumanMessage(content=msg['content']) if msg['type'] == 'human' 
                else AIMessage(content=msg['content'])
                for msg in chat_hist_data
            ]
        context = ""
        NEED_RETRIEVAL = should_retrieve(user_query, chat_hist, llm2)

        if NEED_RETRIEVAL:
            # Call the function from embedding.py
            context_list = similar_embedding(user_query)
            print(context_list)
            context = "\n---\n".join(context_list)
            print(context)
        # 3. Invoke LLM
        prompt = chat_template.invoke({
            'chat_hist': chat_hist,
            'query': user_query, 
            'context': context
        })
        print(NEED_RETRIEVAL)

        def stream_response():
            full_response = ""
            for chunk in llm.stream(prompt):
                token = chunk.content
                full_response += token
                clean_token = re.sub(r'(\*|_)+', '', token)
                yield clean_token  # send partial text immediately
            # Save chat to session after streaming completes
            chat_hist_data.append({'type': 'human', 'content': user_query})
            chat_hist_data.append({'type': 'ai', 'content': full_response})
            request.session['chat_hist'] = chat_hist_data
            request.session.modified = True

        return StreamingHttpResponse(stream_response(), content_type='text/plain')
    except Exception as e:
        print(f"\n[Chatbot View Error]: {e}\n")
        return JsonResponse({'error': 'An internal error occurred processing your request.'}, status=500)
    



def dashboard(request):
        
        file_path = request.session.get("pdf_path")
        file_name = request.session.get("pdf_name")
        quiz_list=[]
        flashcard_list=[]

        def generate_flashcards():
            flashobj = flash(file_path)
            return flashobj.generate_flashcard()

        def generate_quiz():
            quizobj = QuizBuilder(file_path)
            return quizobj.generate_quiz()
        
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = {
                executor.submit(generate_flashcards): "flashcards",
                executor.submit(generate_quiz): "quiz"
            }

            for future in as_completed(futures):
                task = futures[future]
                try:
                    result = future.result()
                    if task == "flashcards":
                        flashcard_list = result
                        request.session['flashcards'] = flashcard_list
                    
                    else:
                        quiz_list = result
                        request.session['quiz'] = quiz_list
                        
                except Exception as e:
                    print(f"{task} failed due to {e}")

        return render(request,'dashboard.html',{'pdf_name':file_name})

def flashcards_view(request):
    flashcards = request.session.get('flashcards', [])
    return render(request, 'flashcards.html', {'flashcards': flashcards})

def quiz_view(request):
    quiz= request.session.get('quiz',[])
    return render(request, 'quiz.html', {'quiz': quiz})
