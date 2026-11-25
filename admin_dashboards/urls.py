from django.urls import path
from admin_dashboards.views import *

app_name = "admin_dash"

urlpatterns = [
    path("", admin_dashboard, name="home"),
    path("users/", user_management, name="users"),
    path("cases/", case_monitoring, name="cases"),
    path("categories/", category_management, name="categories"),
    path("fees/", fee_configuration, name="fees"),
    path("payments/", payment_monitoring, name="payments"),
    path("complaints/", complaint_management, name="complaints"),
    path("content/", content_management, name="content"),
    path("settings/", platform_settings, name="settings"),
    path("audit-logs/", audit_log_management, name="audit_logs"),
    path("security/", security_monitoring, name="security"),
    path("reports/", system_reports, name="reports"),
]
