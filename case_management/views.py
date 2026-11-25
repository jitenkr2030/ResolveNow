"""Case Management views."""
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
def case_management_dashboard(request, *args, **kwargs):
    """View: case_management_dashboard."""
    context = build_page_context(request, "case_management", "case_management_dashboard")
    context["page_title"] = "Case Management Dashboard"
    try:
        return render(request, "case_management/dashboard.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def case_transfer(request, *args, **kwargs):
    """View: case_transfer."""
    context = build_page_context(request, "case_management", "case_transfer")
    context["page_title"] = "Case Transfer"
    try:
        return render(request, "case_management/transfer.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def withdrawal_request(request, *args, **kwargs):
    """View: withdrawal_request."""
    context = build_page_context(request, "case_management", "withdrawal_request")
    context["page_title"] = "Withdrawal Request"
    try:
        return render(request, "case_management/withdrawal_request.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def reopening_request(request, *args, **kwargs):
    """View: reopening_request."""
    context = build_page_context(request, "case_management", "reopening_request")
    context["page_title"] = "Reopening Request"
    try:
        return render(request, "case_management/reopening_request.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def case_notes(request, *args, **kwargs):
    """View: case_notes."""
    context = build_page_context(request, "case_management", "case_notes")
    context["page_title"] = "Case Notes"
    try:
        return render(request, "case_management/notes.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def case_reminders(request, *args, **kwargs):
    """View: case_reminders."""
    context = build_page_context(request, "case_management", "case_reminders")
    context["page_title"] = "Case Reminders"
    try:
        return render(request, "case_management/reminders.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def withdrawal_requests_list(request, *args, **kwargs):
    """View: withdrawal_requests_list."""
    context = build_page_context(request, "case_management", "withdrawal_requests_list")
    context["page_title"] = "Withdrawal Requests List"
    try:
        return render(request, "case_management/withdrawal_requests.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def reopening_requests_list(request, *args, **kwargs):
    """View: reopening_requests_list."""
    context = build_page_context(request, "case_management", "reopening_requests_list")
    context["page_title"] = "Reopening Requests List"
    try:
        return render(request, "case_management/reopening_requests.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

