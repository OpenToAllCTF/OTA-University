from .base_view import *
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required


@login_required()
def index(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()

    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'misc/upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'misc/upload.html')