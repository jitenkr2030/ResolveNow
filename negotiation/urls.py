from django.urls import path
from negotiation.views import *

app_name = "negotiation"

urlpatterns = [
    path("", negotiation_dashboard, name="dashboard"),
    path("<int:dispute_id>/room/", negotiation_room, name="room"),
    path("<int:dispute_id>/proposal/create/", proposal_create, name="proposal_create"),
    path("<int:proposal_id>/", proposal_detail, name="proposal_detail"),
    path("<int:proposal_id>/accept/", proposal_accept, name="proposal_accept"),
    path("<int:proposal_id>/reject/", proposal_reject, name="proposal_reject"),
    path("<int:proposal_id>/counter/", proposal_counter, name="proposal_counter"),
    path("<int:proposal_id>/withdraw/", proposal_withdraw, name="proposal_withdraw"),
    path("<int:dispute_id>/history/", negotiation_history, name="history"),
]
