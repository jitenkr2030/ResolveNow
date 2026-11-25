"""Root URL configuration for ResolveNow platform."""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView, RedirectView
from accounts.views import ResolveNowLoginView
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("user-profiles/", include("user_profiles.urls")),
    path("organizations/", include("organizations.urls")),
    path("verification/", include("verification.urls")),
    path("disputes/", include("disputes.urls")),
    path("case-management/", include("case_management.urls")),
    path("categories/", include("dispute_categories.urls")),
    path("negotiation/", include("negotiation.urls")),
    path("messaging/", include("messaging.urls")),
    path("documents/", include("documents.urls")),
    path("mediators/", include("mediators.urls")),
    path("mediator-assignment/", include("mediator_assignment.urls")),
    path("scheduling/", include("scheduling.urls")),
    path("mediation-sessions/", include("mediation_sessions.urls")),
    path("settlements/", include("settlements.urls")),
    path("digital-signatures/", include("digital_signatures.urls")),
    path("payments/", include("payments.urls")),
    path("subscriptions/", include("subscriptions.urls")),
    path("notifications/", include("notifications.urls")),
    path("grievances/", include("grievances.urls")),
    path("legal-compliance/", include("legal_compliance.urls")),
    path("analytics/", include("analytics.urls")),
    path("ai-assistant/", include("ai_assistant.urls")),
    # Top-level dashboards / portals
    path("", TemplateView.as_view(template_name="landing.html"), name="home"),
    path("dashboard/", include("core_dashboards.urls")),
    path("admin-dashboard/", include("admin_dashboards.urls")),
    path("mediator-portal/", include("mediator_portals.urls")),
    path("legal-portal/", include("legal_portals.urls")),
    path("business-portal/", include("business_portals.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
