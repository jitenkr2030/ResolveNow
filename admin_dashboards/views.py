"""Admin dashboards views (Section 18 - Admin & Super Admin Dashboard)."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Sum, Q, Avg
from django.utils import timezone
from datetime import timedelta

from accounts.models import User, LoginHistory, AccountDeletionRequest
from disputes.models import Dispute, DisputeTimelineEntry
from dispute_categories.models import DisputeCategory
from payments.models import Payment, RefundRequest, TaxInvoice
from grievances.models import Complaint
from mediators.models import MediatorProfile
from organizations.models import Organization
from audit_logs.models import AuditLog
from legal_compliance.models import SecurityIncident, ConsentRecord, DataSubjectRequest
from messaging.models import Notification
from analytics.models import AnalyticsSnapshot


def is_admin(user):
    return user.is_authenticated and (
        user.role in {User.Role.ADMINISTRATOR, User.Role.SUPER_ADMIN} or user.is_superuser
    )


def build_page_context(request, app_name, view_name):
    return {
        "request": request,
        "current_app": app_name,
        "current_view": view_name,
        "feature_title": view_name.replace("_", " ").title(),
    }


@login_required
def admin_dashboard(request, *args, **kwargs):
    if not is_admin(request.user):
        messages.error(request, "Access denied. Administrator privileges required.")
        return redirect("dashboard:home")

    today = timezone.now().date()
    last_30 = timezone.now() - timedelta(days=30)

    stats = {
        "total_users": User.objects.count(),
        "total_disputes": Dispute.objects.count(),
        "pending_applications": Dispute.objects.filter(status="submitted").count(),
        "active_cases": Dispute.objects.exclude(
            status__in=["closed", "withdrawn", "rejected", "draft"]
        ).count(),
        "unassigned_cases": Dispute.objects.filter(
            status="eligible_for_mediation",
            assigned_mediator__isnull=True,
        ).count(),
        "registered_mediators": MediatorProfile.objects.count(),
        "verified_mediators": MediatorProfile.objects.filter(approval_status="approved").count(),
        "pending_mediator_verifications": MediatorProfile.objects.filter(
            approval_status="pending"
        ).count(),
        "organizations": Organization.objects.count(),
        "verified_organizations": Organization.objects.filter(verification_status="verified").count(),
        "complaints_open": Complaint.objects.exclude(
            status__in=["closed", "rejected"]
        ).count(),
        "total_revenue": Payment.objects.filter(status="successful").aggregate(
            Sum("total_amount")
        )["total_amount__sum"] or 0,
        "refunds_pending": RefundRequest.objects.filter(status="pending").count(),
        "security_incidents_open": SecurityIncident.objects.exclude(
            status="resolved"
        ).count(),
        "pending_data_requests": DataSubjectRequest.objects.filter(
            status__in=["pending", "verified"]
        ).count(),
        "deletion_requests": AccountDeletionRequest.objects.filter(status="pending").count(),
        "today_new_users": User.objects.filter(date_joined__date=today).count(),
        "today_new_disputes": Dispute.objects.filter(created_at__date=today).count(),
    }

    # Status breakdown
    status_breakdown = (
        Dispute.objects.values("status").annotate(count=Count("id")).order_by("-count")
    )
    category_breakdown = (
        Dispute.objects.values("category__name").annotate(count=Count("id")).order_by("-count")
    )
    recent_audits = AuditLog.objects.all()[:15]
    recent_disputes = Dispute.objects.all()[:10]
    recent_complaints = Complaint.objects.all()[:5]

    context = {
        "stats": stats,
        "status_breakdown": status_breakdown,
        "category_breakdown": category_breakdown,
        "recent_audits": recent_audits,
        "recent_disputes": recent_disputes,
        "recent_complaints": recent_complaints,
    }
    return render(request, "admin_dashboards/home.html", context)


@login_required
def user_management(request, *args, **kwargs):
    if not is_admin(request.user):
        return redirect("dashboard:home")
    role_filter = request.GET.get("role", "")
    qs = User.objects.all()
    if role_filter:
        qs = qs.filter(role=role_filter)
    qs = qs.order_by("-date_joined")
    return render(request, "admin_dashboards/users.html", {
        "users": qs,
        "roles": User.Role.choices,
        "current_role": role_filter,
        "page_title": "User Management",
    })


@login_required
def case_monitoring(request, *args, **kwargs):
    if not is_admin(request.user):
        return redirect("dashboard:home")
    status_filter = request.GET.get("status", "")
    qs = Dispute.objects.all()
    if status_filter:
        qs = qs.filter(status=status_filter)
    qs = qs.order_by("-created_at")
    return render(request, "admin_dashboards/cases.html", {
        "disputes": qs,
        "statuses": Dispute.Status.choices,
        "status_filter": status_filter,
        "page_title": "Case Monitoring",
    })


@login_required
def category_management(request, *args, **kwargs):
    if not is_admin(request.user):
        return redirect("dashboard:home")
    cats = DisputeCategory.objects.all()
    return render(request, "admin_dashboards/categories.html", {
        "categories": cats,
        "page_title": "Category Management",
    })


@login_required
def fee_configuration(request, *args, **kwargs):
    if not is_admin(request.user):
        return redirect("dashboard:home")
    return render(request, "admin_dashboards/fees.html", {
        "page_title": "Fee Configuration",
        "config": request.user  # placeholder
    })


@login_required
def payment_monitoring(request, *args, **kwargs):
    if not is_admin(request.user):
        return redirect("dashboard:home")
    payments = Payment.objects.all().order_by("-created_at")[:50]
    return render(request, "admin_dashboards/payments.html", {
        "payments": payments,
        "page_title": "Payment Monitoring",
    })


@login_required
def complaint_management(request, *args, **kwargs):
    if not is_admin(request.user):
        return redirect("dashboard:home")
    complaints = Complaint.objects.all().order_by("-submitted_at")
    return render(request, "admin_dashboards/complaints.html", {
        "complaints": complaints,
        "page_title": "Complaint Management",
    })


@login_required
def content_management(request, *args, **kwargs):
    if not is_admin(request.user):
        return redirect("dashboard:home")
    return render(request, "admin_dashboards/content.html", {
        "page_title": "Content Management",
    })


@login_required
def platform_settings(request, *args, **kwargs):
    if not is_admin(request.user):
        return redirect("dashboard:home")
    from django.conf import settings as dj_settings
    return render(request, "admin_dashboards/settings.html", {
        "page_title": "Platform Settings",
        "platform_config": dj_settings.RESOLVENOW_CONFIG,
    })


@login_required
def audit_log_management(request, *args, **kwargs):
    if not is_admin(request.user):
        return redirect("dashboard:home")
    logs = AuditLog.objects.all().order_by("-timestamp")[:200]
    return render(request, "admin_dashboards/audit_logs.html", {
        "logs": logs,
        "page_title": "Audit Logs",
    })


@login_required
def security_monitoring(request, *args, **kwargs):
    if not is_admin(request.user):
        return redirect("dashboard:home")
    incidents = SecurityIncident.objects.all().order_by("-detected_at")
    return render(request, "admin_dashboards/security.html", {
        "incidents": incidents,
        "page_title": "Security Monitoring",
    })


@login_required
def system_reports(request, *args, **kwargs):
    if not is_admin(request.user):
        return redirect("dashboard:home")
    snapshots = AnalyticsSnapshot.objects.all()
    return render(request, "admin_dashboards/reports.html", {
        "snapshots": snapshots,
        "page_title": "System Reports",
    })
