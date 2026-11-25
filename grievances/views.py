"""Grievances views."""
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
def grievance_dashboard(request, *args, **kwargs):
    """View: grievance_dashboard."""
    context = build_page_context(request, "grievances", "grievance_dashboard")
    context["page_title"] = "Grievance Dashboard"
    try:
        return render(request, "grievances/dashboard.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def file_complaint(request, *args, **kwargs):
    """View: file_complaint."""
    context = build_page_context(request, "grievances", "file_complaint")
    context["page_title"] = "File Complaint"
    try:
        return render(request, "grievances/file.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def complaint_detail(request, *args, **kwargs):
    """View: complaint_detail."""
    context = build_page_context(request, "grievances", "complaint_detail")
    context["page_title"] = "Complaint Detail"
    try:
        return render(request, "grievances/detail.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def respond_to_complaint(request, *args, **kwargs):
    """View: respond_to_complaint."""
    context = build_page_context(request, "grievances", "respond_to_complaint")
    context["page_title"] = "Respond To Complaint"
    try:
        return render(request, "grievances/respond.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def investigate_complaint(request, *args, **kwargs):
    """View: investigate_complaint."""
    context = build_page_context(request, "grievances", "investigate_complaint")
    context["page_title"] = "Investigate Complaint"
    try:
        return render(request, "grievances/investigate.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def appeal_complaint(request, *args, **kwargs):
    """View: appeal_complaint."""
    context = build_page_context(request, "grievances", "appeal_complaint")
    context["page_title"] = "Appeal Complaint"
    try:
        return render(request, "grievances/appeal.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def assign_complaint(request, *args, **kwargs):
    """View: assign_complaint."""
    context = build_page_context(request, "grievances", "assign_complaint")
    context["page_title"] = "Assign Complaint"
    try:
        return render(request, "grievances/assign.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def resolve_complaint(request, *args, **kwargs):
    """View: resolve_complaint."""
    context = build_page_context(request, "grievances", "resolve_complaint")
    context["page_title"] = "Resolve Complaint"
    try:
        return render(request, "grievances/resolve.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def submit_feedback(request, *args, **kwargs):
    """View: submit_feedback."""
    context = build_page_context(request, "grievances", "submit_feedback")
    context["page_title"] = "Submit Feedback"
    try:
        return render(request, "grievances/feedback.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

