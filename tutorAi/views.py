from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from tutorAi.components.pdf_reader import pdfDocs
from tutorAi.components.quiz import QuizBuilder
from tutorAi import settings
from tutorAi.components.flashcard import flash
from tutorAi.components.embedding import embed_docs
from dotenv import load_dotenv
import os
load_dotenv()

MAX_PDF_PAGE=40




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




            request.session["pdf_path"] = file_path
            request.session["pdf_name"] = pdf_file.name

            return render(request, "dashboard.html", {
                    "pdf_name": pdf_file.name,
                    "pdf_path": file_path
                })
        except Exception as e:
            fs.delete(filename)
            return render(request, "home.html", {
                "error_message": "An error occurred during file processing"
            })

    return render(request, "home.html")

def dashboard(request):
        file_path = request.session.get("pdf_path")
        
        flashobj=flash(file_path)
        flashcard_list=flashobj.generate_flashcard()
        print(flashcard_list)

        quizobj=QuizBuilder(file_path)
        quiz_list=quizobj.generate_quiz()
        print(quiz_list)
        return render(request,'dashboard.html')