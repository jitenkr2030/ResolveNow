from django.urls import path
from notifications.views import *

app_name = "notifications"

urlpatterns = [
    path("", notifications_center, name="dashboard"),
    path("<int:pk>/read/", mark_read, name="mark_read"),
    path("unread/", unread_count, name="unread_count"),
    path("mark-all-read/", mark_all_read, name="mark_all_read"),
    path("preferences/", preferences, name="preferences"),
]
