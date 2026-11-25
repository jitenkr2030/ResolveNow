from django.urls import path
from messaging.views import *

app_name = "messaging"

urlpatterns = [
    path("", message_threads, name="threads"),
    path("<int:dispute_id>/threads/", dispute_threads, name="dispute_threads"),
    path("<int:dispute_id>/thread/create/", thread_create, name="thread_create"),
    path("<int:thread_id>/", thread_detail, name="thread_detail"),
    path("<int:thread_id>/send/", message_send, name="send"),
    path("<int:message_id>/read/", message_mark_read, name="mark_read"),
    path("notifications/", notifications_list, name="notifications"),
    path("notifications/<int:notif_id>/read/", notification_mark_read, name="notification_read"),
    path("preferences/", notification_preferences, name="preferences"),
]
