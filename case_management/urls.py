from django.urls import path
from case_management.views import *

app_name = "case_management"

urlpatterns = [
    path("", case_management_dashboard, name="dashboard"),
    path("<int:dispute_id>/transfer/", case_transfer, name="transfer"),
    path("<int:dispute_id>/withdrawal-request/", withdrawal_request, name="withdrawal_request"),
    path("<int:dispute_id>/reopening-request/", reopening_request, name="reopening_request"),
    path("<int:dispute_id>/notes/", case_notes, name="notes"),
    path("<int:dispute_id>/reminders/", case_reminders, name="reminders"),
    path("withdrawal-requests/", withdrawal_requests_list, name="withdrawal_requests"),
    path("reopening-requests/", reopening_requests_list, name="reopening_requests"),
]
