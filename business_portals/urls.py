from django.urls import path
from business_portals.views import *

app_name = "business_portal"

urlpatterns = [
    path("", business_portal_home, name="home"),
    path("organizations/", business_organizations, name="organizations"),
    path("cases/", business_cases, name="cases"),
    path("reports/", business_reports, name="reports"),
    path("billing/", business_billing, name="billing"),
    path("bulk-import/", business_bulk_import, name="bulk_import"),
]
