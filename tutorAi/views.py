from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from tutorAi.components.pdf_reader import pdfReader
from tutorAi import settings
import os
MAX_PDF_PAGE=40

def upload_pdf(request):
    if request.method== "POST" and request.FILES.get("pdf"):
        pdf_file=request.FILES['pdf']
        fs=FileSystemStorage(location='media/temp')
        filename = fs.save(pdf_file.name, pdf_file)

        file_path = os.path.join(settings.MEDIA_ROOT, 'temp', filename)
        docs,len=pdfReader(file_path)

        print(docs)

        request.session["pdf_path"] = file_path
        request.session["pdf_name"] = pdf_file.name

        return render(request, "dashboard.html", {
                "pdf_name": pdf_file.name,
            })

    return render(request, "home.html")

def dashboard(request):
    return render(request,'dashboard.html')