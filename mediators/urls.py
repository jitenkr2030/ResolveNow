from django.urls import path
from mediators.views import *

app_name = "mediators"

urlpatterns = [
    path("", mediator_directory, name="directory"),
    path("register/", mediator_register, name="register"),
    path("profile/", my_mediator_profile, name="my_profile"),
    path("profile/edit/", mediator_profile_edit, name="profile_edit"),
    path("availability/", mediator_availability, name="availability"),
    path("<int:pk>/", mediator_public_profile, name="public_profile"),
    path("admin/", mediator_admin_list, name="admin_list"),
    path("<int:pk>/approve/", mediator_approve, name="approve"),
    path("<int:pk>/suspend/", mediator_suspend, name="suspend"),
    path("<int:pk>/feedback/", mediator_feedback_submit, name="feedback_submit"),
]
