"""Mediator Assignment views."""
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
def assignment_dashboard(request, *args, **kwargs):
    """View: assignment_dashboard."""
    context = build_page_context(request, "mediator_assignment", "assignment_dashboard")
    context["page_title"] = "Assignment Dashboard"
    try:
        return render(request, "mediator_assignment/dashboard.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def assignment_request_create(request, *args, **kwargs):
    """View: assignment_request_create."""
    context = build_page_context(request, "mediator_assignment", "assignment_request_create")
    context["page_title"] = "Assignment Request Create"
    try:
        return render(request, "mediator_assignment/request.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def assignment_accept(request, *args, **kwargs):
    """View: assignment_accept."""
    context = build_page_context(request, "mediator_assignment", "assignment_accept")
    context["page_title"] = "Assignment Accept"
    try:
        return render(request, "mediator_assignment/accept.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def assignment_reject(request, *args, **kwargs):
    """View: assignment_reject."""
    context = build_page_context(request, "mediator_assignment", "assignment_reject")
    context["page_title"] = "Assignment Reject"
    try:
        return render(request, "mediator_assignment/reject.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def replacement_request(request, *args, **kwargs):
    """View: replacement_request."""
    context = build_page_context(request, "mediator_assignment", "replacement_request")
    context["page_title"] = "Replacement Request"
    try:
        return render(request, "mediator_assignment/replacement.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def assignment_confirm(request, *args, **kwargs):
    """View: assignment_confirm."""
    context = build_page_context(request, "mediator_assignment", "assignment_confirm")
    context["page_title"] = "Assignment Confirm"
    try:
        return render(request, "mediator_assignment/confirm.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def coi_declare(request, *args, **kwargs):
    """View: coi_declare."""
    context = build_page_context(request, "mediator_assignment", "coi_declare")
    context["page_title"] = "Coi Declare"
    try:
        return render(request, "mediator_assignment/coi.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

