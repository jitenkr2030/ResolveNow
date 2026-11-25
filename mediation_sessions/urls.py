from django.urls import path
from mediation_sessions.views import *
from django.views.generic import RedirectView

app_name = "mediation_sessions"

urlpatterns = [
    path("", RedirectView.as_view(url="/disputes/", permanent=False), name="dashboard"),
    path("<int:session_id>/room/", mediation_room, name="room"),
    path("<int:session_id>/join/", join_room, name="join"),
    path("<int:room_id>/participants/", room_participants, name="participants"),
    path("<int:room_id>/notes/", session_notes, name="notes"),
    path("<int:room_id>/caucus/", private_caucus, name="caucus"),
    path("<int:room_id>/recording-consent/", recording_consent, name="recording_consent"),
    path("<int:room_id>/close/", close_room, name="close"),
]
