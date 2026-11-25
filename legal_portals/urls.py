from django.urls import path
from legal_portals.views import *

app_name = "legal_portal"

urlpatterns = [
    path("", legal_portal_home, name="home"),
    path("clients/", client_management, name="clients"),
    path("cases/", legal_cases, name="cases"),
    path("documents/", legal_documents, name="documents"),
    path("authorizations/", client_authorizations, name="authorizations"),
]
