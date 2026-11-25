from django.urls import path
from mediator_portals.views import *

app_name = "mediator_portal"

urlpatterns = [
    path("", mediator_portal_home, name="home"),
    path("cases/", mediator_cases, name="cases"),
    path("schedule/", mediator_schedule, name="schedule"),
    path("earnings/", mediator_earnings, name="earnings"),
    path("feedback/", mediator_feedback, name="feedback"),
]
