"""Analytics views."""
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
def analytics_dashboard(request, *args, **kwargs):
    """View: analytics_dashboard."""
    context = build_page_context(request, "analytics", "analytics_dashboard")
    context["page_title"] = "Analytics Dashboard"
    try:
        return render(request, "analytics/dashboard.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def platform_snapshot(request, *args, **kwargs):
    """View: platform_snapshot."""
    context = build_page_context(request, "analytics", "platform_snapshot")
    context["page_title"] = "Platform Snapshot"
    try:
        return render(request, "analytics/snapshot.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def category_analytics(request, *args, **kwargs):
    """View: category_analytics."""
    context = build_page_context(request, "analytics", "category_analytics")
    context["page_title"] = "Category Analytics"
    try:
        return render(request, "analytics/categories.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def mediator_performance(request, *args, **kwargs):
    """View: mediator_performance."""
    context = build_page_context(request, "analytics", "mediator_performance")
    context["page_title"] = "Mediator Performance"
    try:
        return render(request, "analytics/mediators.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def generate_snapshot(request, *args, **kwargs):
    """View: generate_snapshot."""
    context = build_page_context(request, "analytics", "generate_snapshot")
    context["page_title"] = "Generate Snapshot"
    try:
        return render(request, "analytics/generate.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

