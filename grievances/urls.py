from django.urls import path
from grievances.views import *

app_name = "grievances"

urlpatterns = [
    path("", grievance_dashboard, name="dashboard"),
    path("file/", file_complaint, name="file"),
    path("<int:pk>/", complaint_detail, name="detail"),
    path("<int:pk>/respond/", respond_to_complaint, name="respond"),
    path("<int:pk>/investigate/", investigate_complaint, name="investigate"),
    path("<int:pk>/appeal/", appeal_complaint, name="appeal"),
    path("<int:pk>/assign/", assign_complaint, name="assign"),
    path("<int:pk>/resolve/", resolve_complaint, name="resolve"),
    path("feedback/", submit_feedback, name="feedback"),
]
