from django.urls import path
from analytics.views import *

app_name = "analytics"

urlpatterns = [
    path("", analytics_dashboard, name="dashboard"),
    path("snapshot/", platform_snapshot, name="snapshot"),
    path("categories/", category_analytics, name="categories"),
    path("mediators/", mediator_performance, name="mediators"),
    path("generate/", generate_snapshot, name="generate"),
]
