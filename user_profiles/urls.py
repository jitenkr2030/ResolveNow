from django.urls import path
from user_profiles.views import *

app_name = "user_profiles"

urlpatterns = [
    path("", user_profile_redirect, name="dashboard"),
    path("edit/", user_profile_edit, name="edit"),
    path("completion/", profile_completion, name="completion"),
]
