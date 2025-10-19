from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

def upload_pdf(request):
    if request.method== "POST" and request.FILES.get("pdf"):
        pdf_file=request.FILES['pdf']
        fs=FileSystemStorage(location='media/temp')
        filename = fs.save(pdf_file.name, pdf_file)
        file_path = fs.path(filename)

        request.session["pdf_path"] = file_path
        request.session["pdf_name"] = pdf_file.name

        return render(request, "dashboard.html", {
                "pdf_name": pdf_file.name,
            })

    return render(request, "home.html")

def dashboard(request):
    return render(request,'dashboard.html')