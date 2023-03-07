from django.contrib import admin
from .models import Document, Request, Client

# Register your models here.

admin.site.register(Document)
admin.site.register(Request)
admin.site.register(Client)
