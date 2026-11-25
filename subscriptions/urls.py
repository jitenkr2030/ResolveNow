from django.urls import path
from subscriptions.views import *

app_name = "subscriptions"

urlpatterns = [
    path("", subscriptions_dashboard, name="dashboard"),
    path("plans/", plans_list, name="plans"),
    path("subscribe/<int:plan_id>/", subscribe, name="subscribe"),
    path("api-keys/", api_keys, name="api_keys"),
    path("api-keys/create/", api_key_create, name="api_key_create"),
    path("bulk-import/", bulk_import, name="bulk_import"),
]
