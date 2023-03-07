from django.urls import path, include, re_path
from .views import clients, requests, documents, client_view_doc, client_view, request_view, choose_request, client_auth, client_pin, doc_form, show_file, client_view_request

urlpatterns = [
    # Links for RM facing interface
    re_path(r'^client/$', client_view, name="client_view"),
    re_path(r'^client/request/$', client_view_request,
            name="client_view_request"),
    re_path(r'^client/document/$', client_view_doc,
            name="client_view_doc"),
    re_path(r'^request/(?P<request_id>\d+)/$', request_view,
            name="request_view"),  # specif view for the chosen client
    re_path(r'^choose_request/$', choose_request, name="choose_request"),
    path('', clients, name="clients"),  # this represents the dashboard
    path('requests', requests, name="requests"),
    path('documents', documents, name="documents"),
    re_path(r'^managers/files/$', show_file, name='show_file'),

    # Links for Client facing interface
    path('client_auth', client_auth, name="client_auth"),
    path('client_pin', client_pin, name="client_pin"),
    path('doc_form', doc_form, name='doc_form'),
]
