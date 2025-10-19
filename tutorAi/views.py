from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from tutorAi.components.pdf_reader import pdfReader
from tutorAi import settings
from tutorAi.components.flashcard import flash
import os

MAX_PDF_PAGE=40

def upload_pdf(request):
    if request.method== "POST" and request.FILES.get("pdf"):
        pdf_file=request.FILES['pdf']
        fs=FileSystemStorage(location='media/temp')
        filename = fs.save(pdf_file.name, pdf_file)

        file_path = os.path.join(settings.MEDIA_ROOT, 'temp', filename)
        

        try:
            docs,page_count=pdfReader(file_path)
            if page_count>MAX_PDF_PAGE:
                fs.delete(filename)
                return render(request,'home.html',{
                    "error_message": f"PDF is too large. Max pages allowed is {MAX_PDF_PAGE}, but your file has {page_count} pages."
                })
        

            print(docs)

            flashobj=flash(file_path)
            flashcard_list=flashobj.generate_flashcard()
            print(flashcard_list)

            request.session["pdf_path"] = file_path
            request.session["pdf_name"] = pdf_file.name

            return render(request, "dashboard.html", {
                    "pdf_name": pdf_file.name,
                })
        except Exception as e:
            fs.delete(filename)
            return render(request, "home.html", {
                "error_message": "An error occurred during file processing"
            })

    return render(request, "home.html")

def dashboard(request):
    return render(request,'dashboard.html')