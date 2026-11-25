from django.urls import path
from legal_compliance.views import *

app_name = "legal_compliance"

urlpatterns = [
    path("", compliance_dashboard, name="dashboard"),
    path("consents/", consent_records, name="consents"),
    path("data-requests/", data_subject_requests, name="data_requests"),
    path("data-requests/create/", data_subject_request_create, name="data_request_create"),
    path("retention-policies/", retention_policies, name="retention"),
    path("incidents/", security_incidents, name="incidents"),
    path("coi/", user_coi_declarations, name="coi"),
]
