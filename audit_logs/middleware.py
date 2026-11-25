"""Audit log middleware (Section 20)."""
from django.utils import timezone
from django.conf import settings
from .models import AuditLog


class AuditLogMiddleware:
    """Logs sensitive requests to the audit log."""

    SENSITIVE_PATHS = (
        "/admin/",
        "/accounts/login/",
        "/accounts/logout/",
        "/disputes/create/",
        "/disputes/submit/",
        "/payments/",
        "/documents/upload/",
        "/admin-dashboard/",
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Only log sensitive paths to avoid huge volume
        path = request.path or ""
        if not any(path.startswith(p) for p in self.SENSITIVE_PATHS):
            return response
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            return response
        xff = request.META.get("HTTP_X_FORWARDED_FOR")
        ip = (xff.split(",")[0] if xff else None) or request.META.get("REMOTE_ADDR")
        AuditLog.objects.create(
            actor=user,
            action=AuditLog.Action.OTHER,
            resource_type="HTTP",
            description=f"{request.method} {path}",
            request_path=path,
            request_method=request.method,
            status_code=response.status_code,
            ip_address=ip,
            user_agent=request.META.get("HTTP_USER_AGENT", "")[:500],
            session_key=request.session.session_key or "",
        )
        return response
