# Author Tinotenda Kurimwi 06 March 2023

from django.shortcuts import render, redirect, get_object_or_404
from .models import Client, Document, Request
from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from .forms import DocumentForm
import datetime
import os
import mimetypes


def clients(request):
    """ This function handles the creation of clients
      as well as viewing all clients together 
      User Creation Form Parameters
      @param: name 
      @param: surname 
      @param: email 
      """
    if request.method == 'POST':
        if request.POST.get('name'):
            client = Client()
            client.name = request.POST.get('name')
            client.surname = request.POST.get('surname')
            client.email = request.POST.get('email')
            client.save()
        clients = Client.objects.all()
        return render(request, 'clients.html', {"clients": clients})
    else:
        clients = Client.objects.all()
        return render(request, 'clients.html', {"clients": clients})


def requests(request):
    """ This function handles the creation of requests
      as well as viewing all requests together 
      Request Creation Form Parameters
      @param: request (the name of the request) 
      @param: client_id  
      """
    if request.method == 'POST':
        if request.POST.get('request'):
            request_object = Request()
            request_object.name = request.POST.get('request')
            request_object.submitted = False
            request_object.date_submitted = datetime.datetime.now()
            request_object.client_id = request.POST.get('client_id')
            request_object.save()
        clients = Client.objects.all()
        requests = Request.objects.all()
        return render(request, 'requests.html', {"requests": requests, "clients": clients})
    else:
        clients = Client.objects.all()
        requests = Request.objects.all()
        return render(request, 'requests.html', {"requests": requests, "clients": clients})


def documents(request):
    documents = Document.objects.all()
    return render(request, 'documents.html', {"documents": documents})


def client_view(request):
    """ This function handles the updating of client's information, 
    as well as deleting a client which deletes all data 
    Client Update Form Parameters
    @param: client_id
    @param: name 
    @param: surname  
    @param: email  

    Client Delete Form Parameters
    @param: delete_id (this is the client id)
    """
    if request.method == 'POST':
        if request.POST.get('delete_id'):
            client = Client()
            client.id = request.POST.get('delete_id')
            client.delete()
            clients = Client.objects.all()
            return render(request, 'clients.html', {"clients": clients})
        elif request.POST.get('name'):
            client = Client()
            client_id = request.POST.get('client_id')
            client.id = client_id
            client.name = request.POST.get('name')
            client.surname = request.POST.get('surname')
            client.email = request.POST.get('email')
            client.save()

        client_id = request.POST.get('client_id')
        clients = Client.objects.filter(id=client_id)
        for client in clients:
            documents = client.documents.all()
            requests = client.requests.all()
        return render(request, 'client_view.html', {"requests": requests, "clients": clients, "documents": documents})


def client_view_request(request):
    """ This function handles the updating of request information, 
        as well as deleting a request which deletes all files 
        Request Update Form Parameters
        @param: request_id
        @param: name 

        Request Delete Form Parameters
        @param: delete_id (this is the request id)
    """
    if request.method == 'POST':
        if request.POST.get('delete_id'):
            request_object = Request()
            request_object.id = request.POST.get('delete_id')
            request_object = Request.objects.get(id=request_object.id)
            clients = Client.objects.filter(id=request_object.client.id)
            request_object.delete()
            for client in clients:
                documents = client.documents.all()
                requests = client.requests.all()
            return render(request, 'client_view.html', {"requests": requests, "clients": clients, "documents": documents})
        elif request.POST.get('name'):
            request_object = Request()
            request_object.id = request.POST.get('request_id')
            request_object.name = request.POST.get('name')
            request_object.save(update_fields=['name'])
            request_object = Request.objects.get(id=request_object.id)

        request_object_id = request.POST.get('request_id')
        request_object = Request.objects.get(id=request_object_id)
        clients = Client.objects.filter(id=request_object.client.id)
        for client in clients:
            documents = client.documents.all()
            requests = client.requests.all()
        return render(request, 'client_view.html', {"requests": requests, "clients": clients, "documents": documents})


def client_view_doc(request):
    if request.method == 'POST':
        if request.POST.get('delete_id'):
            document_id = request.POST.get('delete_id')
            client_id = Document.objects.get(id=document_id).client.id
            clients = Client.objects.filter(id=client_id)
            for client in clients:
                documents = client.documents.all()
                requests = client.requests.all()
            document = Document()
            document.id = request.POST.get('delete_id')
            document.delete()
            return render(request, 'client_view.html', {"requests": requests, "clients": clients, "documents": documents})
        else:
            clients = Client.objects.all()
            return render(request, 'clients.html', {"clients": clients})


def choose_request(request):
    return redirect('request_view', request_id=request.POST.get('request_id', 0))


def request_view(request, request_id):
    request_id = get_object_or_404(Request, pk=request_id)
    request_id = request_id.id
    requests = Request.objects.filter(id=request_id)
    for request_object in requests:
        documents = request_object.documents.all()
    return render(request, 'request_view.html', {"requests": requests, "documents": documents})


def client_auth(request):
    if request.method == 'POST':
        if request.POST.get('email'):
            client_email = request.POST.get('email')
            client = Client.objects.get(email=client_email)
            return render(request, 'client_pin.html', {"client_id": client.id})
    else:
        return render(request, 'client_auth.html')


def client_pin(request):
    if request.method == 'POST':
        client_id = request.POST.get('client_id')
        clients = Client.objects.filter(id=client_id)
        for client in clients:
            requests = client.requests.filter(submitted=False)
        document = DocumentForm()
        return render(request, "doc_form.html", {'requests': requests, 'client_id': client_id, "form": document})
    else:
        return render(request, 'client_auth.html')


def doc_form(request):
    """ This function handles the uploading of the files, 
        the user can upload files recursively 
        Retrieve File Parameters
        @param: File
        @param: client_id
        @param: request_id

    """
    if request.method == 'POST':
        document = DocumentForm(request.POST, request.FILES)
        if document.is_valid():
            document_object = Document()
            document_object.name = request.FILES['file'].name
            document_object.document = request.FILES['file']
            document_object.date = datetime.datetime.now()
            document_object.client_id = request.POST.get('client_id')
            document_object.request_id = request.POST.get('request_id')
            document_object.save()

            request_object = Request()
            request_object.id = request.POST.get('request_id')
            request_object.submitted = True
            request_object.save(update_fields=['submitted'])

        client_id = request.POST.get('client_id')
        clients = Client.objects.filter(id=client_id)
        for client in clients:
            requests = client.requests.all()
        document = DocumentForm()
        return render(request, "doc_form.html", {'requests': requests, 'client_id': client_id, "form": document})
    else:
        return render(request, 'client_auth.html')


def show_file(request):
    """ This function handles the viewing of PDFs, 
        else it simply downloads the file
        Retrieve File Parameters
        @param: name (file name)

    """
    if request.method == 'POST':
        filename = request.POST.get('name')
        filepath = os.path.join('', filename)
        if(filepath[-3:] == "pdf"):
            return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filepath = os.path.join(BASE_DIR, filename)
        with open(filepath, 'rb') as f:
            path = f.read()
            mime_type, _ = mimetypes.guess_type(filepath)
            response = HttpResponse(path, content_type=mime_type)
            response['Content-Disposition'] = "attachment; filename=%s" % filename
            return response
