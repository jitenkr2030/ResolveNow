from django.urls import path
from documents.views import *

app_name = "documents"

urlpatterns = [
    path("", document_list, name="list"),
    path("<int:dispute_id>/", dispute_documents, name="dispute_documents"),
    path("<int:dispute_id>/upload/", document_upload, name="upload"),
    path("<int:pk>/", document_detail, name="detail"),
    path("<int:pk>/download/", document_download, name="download"),
    path("<int:pk>/preview/", document_preview, name="preview"),
    path("<int:pk>/replace/", document_replace, name="replace"),
    path("<int:pk>/share/", document_share, name="share"),
    path("<int:pk>/delete/", document_delete, name="delete"),
    path("<int:pk>/versions/", document_versions, name="versions"),
    path("<int:dispute_id>/folders/", document_folders, name="folders"),
    path("<int:dispute_id>/folders/create/", folder_create, name="folder_create"),
]
