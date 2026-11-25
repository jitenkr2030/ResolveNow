"""Mediator Portals views."""
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
def mediator_portal_home(request, *args, **kwargs):
    """View: mediator_portal_home."""
    context = build_page_context(request, "mediator_portals", "mediator_portal_home")
    context["page_title"] = "Mediator Portal Home"
    try:
        return render(request, "mediator_portals/home.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def mediator_cases(request, *args, **kwargs):
    """View: mediator_cases."""
    context = build_page_context(request, "mediator_portals", "mediator_cases")
    context["page_title"] = "Mediator Cases"
    try:
        return render(request, "mediator_portals/cases.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def mediator_schedule(request, *args, **kwargs):
    """View: mediator_schedule."""
    context = build_page_context(request, "mediator_portals", "mediator_schedule")
    context["page_title"] = "Mediator Schedule"
    try:
        return render(request, "mediator_portals/schedule.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def mediator_earnings(request, *args, **kwargs):
    """View: mediator_earnings."""
    context = build_page_context(request, "mediator_portals", "mediator_earnings")
    context["page_title"] = "Mediator Earnings"
    try:
        return render(request, "mediator_portals/earnings.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def mediator_feedback(request, *args, **kwargs):
    """View: mediator_feedback."""
    context = build_page_context(request, "mediator_portals", "mediator_feedback")
    context["page_title"] = "Mediator Feedback"
    try:
        return render(request, "mediator_portals/feedback.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

