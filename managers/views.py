from django.shortcuts import render, redirect, get_object_or_404
from .models import Client, Document, Request
from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from .forms import DocumentForm
from .functions.functions import handle_uploaded_file
import datetime
import os
# Create your views here.


def clients(request):
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


def chose_client(request):
    return redirect('client_view', client_id=request.POST.get('client_id', 0))


def client_view(request):
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
            clients = Client.objects.filter(id=client_id)
            for client in clients:
                documents = client.documents.all()
                requests = client.requests.all()
            return render(request, 'client_view.html', {"requests": requests, "clients": clients, "documents": documents})
        else:
            client_id = request.POST.get('client_id')
            clients = Client.objects.filter(id=client_id)
            requests = []
            documents = []
            for client in clients:
                documents = client.documents.all()
                requests = client.requests.all()
            return render(request, 'client_view.html', {"requests": requests, "clients": clients, "documents": documents})


def client_view_request(request):
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

            clients = Client.objects.filter(id=request_object.client.id)
            for client in clients:
                documents = client.documents.all()
                requests = client.requests.all()
            return render(request, 'client_view.html', {"requests": requests, "clients": clients, "documents": documents})
        else:
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
            handle_uploaded_file(request.FILES['file'])
        client_id = request.POST.get('client_id')
        clients = Client.objects.filter(id=client_id)
        for client in clients:
            requests = client.requests.filter()
        document = DocumentForm()
        return render(request, "doc_form.html", {'requests': requests, 'client_id': client_id, "form": document})
    else:
        return render(request, 'client_auth.html')


def show_file(request):
    if request.method == 'POST':
        filepath = os.path.join('', request.POST.get('name'))
        return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
