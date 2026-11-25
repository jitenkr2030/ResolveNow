from django.urls import path
from core_dashboards.views import *

app_name = "dashboard"

urlpatterns = [
    path("", user_dashboard, name="home"),
    path("individual/", individual_dashboard, name="individual"),
    path("claims/", my_claims_dashboard, name="my_claims"),
    path("responses/", my_responses_dashboard, name="my_responses"),
]
