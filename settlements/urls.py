from django.urls import path
from settlements.views import *
from django.views.generic import RedirectView

app_name = "settlements"

urlpatterns = [
    path("", RedirectView.as_view(url="/disputes/", permanent=False), name="dashboard"),
    path("<int:dispute_id>/create/", settlement_create, name="create"),
    path("<int:pk>/", settlement_detail, name="detail"),
    path("<int:pk>/sign/", settlement_sign, name="sign"),
    path("<int:pk>/generate-doc/", generate_settlement_doc, name="generate_doc"),
    path("<int:pk>/compliance/", compliance_tracking, name="compliance"),
    path("<int:compliance_id>/mark-met/", mark_compliance_met, name="mark_compliance_met"),
]
