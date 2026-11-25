from django.urls import path
from mediator_assignment.views import *

app_name = "mediator_assignment"

urlpatterns = [
    path("", assignment_dashboard, name="dashboard"),
    path("<int:dispute_id>/request/", assignment_request_create, name="request"),
    path("<int:request_id>/accept/", assignment_accept, name="accept"),
    path("<int:request_id>/reject/", assignment_reject, name="reject"),
    path("<int:dispute_id>/replacement/", replacement_request, name="replacement"),
    path("<int:request_id>/confirm/", assignment_confirm, name="confirm"),
    path("coi/<int:dispute_id>/", coi_declare, name="coi"),
]
