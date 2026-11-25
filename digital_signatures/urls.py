from django.urls import path
from digital_signatures.views import *

app_name = "digital_signatures"

urlpatterns = [
    path("request/", signature_request, name="request"),
    path("<int:pk>/sign/", signature_sign, name="sign"),
    path("<int:pk>/verify/", signature_verify, name="verify"),
    path("history/", signature_history, name="history"),
]
