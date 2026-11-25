from django.urls import path
from organizations.views import *

app_name = "organizations"

urlpatterns = [
    path("", organization_list, name="list"),
    path("create/", organization_create, name="create"),
    path("<int:pk>/", organization_detail, name="detail"),
    path("<int:pk>/edit/", organization_edit, name="edit"),
    path("<int:pk>/members/", organization_members, name="members"),
    path("<int:pk>/invite/", organization_invite, name="invite"),
    path("<int:pk>/verify/", organization_verify, name="verify"),
    path("<int:pk>/subscription/", organization_subscription, name="subscription"),
]
