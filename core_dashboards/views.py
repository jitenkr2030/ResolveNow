"""Core dashboards views - main user dashboard (Section 22 - user roles)."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum, Q, Avg
from django.utils import timezone
from datetime import timedelta

from accounts.models import User
from disputes.models import Dispute, DisputeTimelineEntry
from dispute_categories.models import DisputeCategory
from documents.models import Document
from payments.models import Payment
from messaging.models import Notification
from scheduling.models import ScheduledSession


def build_page_context(request, app_name, view_name):
    return {
        "request": request,
        "current_app": app_name,
        "current_view": view_name,
        "feature_title": view_name.replace("_", " ").title(),
    }


@login_required
def user_dashboard(request, *args, **kwargs):
    """Main dashboard routing based on user role."""
    user = request.user
    # Compute global stats for the user
    my_filed = Dispute.objects.filter(claimant=user)
    my_participations = Dispute.objects.filter(parties__user=user).distinct()
    my_documents = Document.objects.filter(uploaded_by=user)
    my_payments = Payment.objects.filter(user=user)
    my_notifications = Notification.objects.filter(recipient=user, is_read=False)
    upcoming_sessions = ScheduledSession.objects.filter(
        Q(dispute__claimant=user) | Q(dispute__parties__user=user),
        scheduled_start__gte=timezone.now(),
        status="scheduled",
    ).distinct().order_by("scheduled_start")[:5]
    recent_timeline = DisputeTimelineEntry.objects.filter(
        dispute__in=my_participations
    ).order_by("-created_at")[:5]

    # Role-specific stats
    if user.role == User.Role.MEDIATOR:
        from mediators.models import MediatorProfile
        try:
            mediator_profile = user.mediator_profile
            assigned_cases = Dispute.objects.filter(assigned_mediator=mediator_profile)
            upcoming_sessions = ScheduledSession.objects.filter(
                mediator=mediator_profile,
                scheduled_start__gte=timezone.now(),
                status="scheduled",
            ).order_by("scheduled_start")[:5]
        except MediatorProfile.DoesNotExist:
            assigned_cases = []
    else:
        assigned_cases = []

    context = {
        "page_title": "Dashboard",
        "my_filed": my_filed,
        "my_participations": my_participations,
        "my_documents": my_documents,
        "my_payments": my_payments,
        "my_notifications": my_notifications,
        "upcoming_sessions": upcoming_sessions,
        "recent_timeline": recent_timeline,
        "assigned_cases": assigned_cases,
        "stats": {
            "filed": my_filed.count(),
            "participating": my_participations.count(),
            "documents": my_documents.count(),
            "notifications": my_notifications.count(),
            "active": my_participations.exclude(status__in=["closed", "withdrawn", "rejected"]).count(),
            "completed": my_participations.filter(status__in=["closed", "settlement_accepted"]).count(),
        },
        "categories": DisputeCategory.objects.filter(is_active=True)[:6],
    }
    return render(request, "core_dashboards/home.html", context)


@login_required
def individual_dashboard(request, *args, **kwargs):
    user = request.user
    filed = Dispute.objects.filter(claimant=user).order_by("-created_at")[:10]
    participating = Dispute.objects.filter(parties__user=user).order_by("-created_at")[:10]
    return render(request, "core_dashboards/individual.html", {
        "filed": filed,
        "participating": participating,
        "page_title": "Individual Dashboard",
    })


@login_required
def my_claims_dashboard(request, *args, **kwargs):
    user = request.user
    filed = Dispute.objects.filter(claimant=user).order_by("-created_at")
    return render(request, "core_dashboards/my_claims.html", {
        "disputes": filed,
        "page_title": "My Claims",
    })


@login_required
def my_responses_dashboard(request, *args, **kwargs):
    user = request.user
    responses = Dispute.objects.filter(parties__user=user, parties__role="respondent").order_by("-created_at")
    return render(request, "core_dashboards/my_responses.html", {
        "disputes": responses,
        "page_title": "My Responses",
    })
