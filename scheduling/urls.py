from django.urls import path
from scheduling.views import *

app_name = "scheduling"

urlpatterns = [
    path("", scheduling_dashboard, name="dashboard"),
    path("<int:dispute_id>/schedule/", session_schedule, name="schedule"),
    path("<int:session_id>/", session_detail, name="session_detail"),
    path("<int:session_id>/reschedule/", session_reschedule, name="reschedule"),
    path("<int:session_id>/cancel/", session_cancel, name="cancel"),
    path("<int:session_id>/complete/", session_complete, name="complete"),
    path("<int:session_id>/participants/", session_participants, name="participants"),
    path("my-calendar/", my_calendar, name="my_calendar"),
]
