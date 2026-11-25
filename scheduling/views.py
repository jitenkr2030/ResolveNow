"""Scheduling views."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView, View
from django.http import HttpResponseForbidden, JsonResponse, Http404


def build_page_context(request, app_name, view_name):
    """Shared context for feature pages."""
    return {
        "request": request,
        "current_app": app_name,
        "current_view": view_name,
        "feature_title": view_name.replace("_", " ").title(),
    }


@login_required
def scheduling_dashboard(request, *args, **kwargs):
    """View: scheduling_dashboard."""
    context = build_page_context(request, "scheduling", "scheduling_dashboard")
    context["page_title"] = "Scheduling Dashboard"
    try:
        return render(request, "scheduling/dashboard.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def session_schedule(request, *args, **kwargs):
    """View: session_schedule."""
    context = build_page_context(request, "scheduling", "session_schedule")
    context["page_title"] = "Session Schedule"
    try:
        return render(request, "scheduling/schedule.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def session_detail(request, *args, **kwargs):
    """View: session_detail."""
    context = build_page_context(request, "scheduling", "session_detail")
    context["page_title"] = "Session Detail"
    try:
        return render(request, "scheduling/session_detail.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def session_reschedule(request, *args, **kwargs):
    """View: session_reschedule."""
    context = build_page_context(request, "scheduling", "session_reschedule")
    context["page_title"] = "Session Reschedule"
    try:
        return render(request, "scheduling/reschedule.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def session_cancel(request, *args, **kwargs):
    """View: session_cancel."""
    context = build_page_context(request, "scheduling", "session_cancel")
    context["page_title"] = "Session Cancel"
    try:
        return render(request, "scheduling/cancel.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def session_complete(request, *args, **kwargs):
    """View: session_complete."""
    context = build_page_context(request, "scheduling", "session_complete")
    context["page_title"] = "Session Complete"
    try:
        return render(request, "scheduling/complete.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def session_participants(request, *args, **kwargs):
    """View: session_participants."""
    context = build_page_context(request, "scheduling", "session_participants")
    context["page_title"] = "Session Participants"
    try:
        return render(request, "scheduling/participants.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def my_calendar(request, *args, **kwargs):
    """View: my_calendar."""
    context = build_page_context(request, "scheduling", "my_calendar")
    context["page_title"] = "My Calendar"
    try:
        return render(request, "scheduling/my_calendar.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

