"""Subscriptions views."""
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
def subscriptions_dashboard(request, *args, **kwargs):
    """View: subscriptions_dashboard."""
    context = build_page_context(request, "subscriptions", "subscriptions_dashboard")
    context["page_title"] = "Subscriptions Dashboard"
    try:
        return render(request, "subscriptions/dashboard.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def plans_list(request, *args, **kwargs):
    """View: plans_list."""
    context = build_page_context(request, "subscriptions", "plans_list")
    context["page_title"] = "Plans List"
    try:
        return render(request, "subscriptions/plans.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def subscribe(request, *args, **kwargs):
    """View: subscribe."""
    context = build_page_context(request, "subscriptions", "subscribe")
    context["page_title"] = "Subscribe"
    try:
        return render(request, "subscriptions/subscribe.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def api_keys(request, *args, **kwargs):
    """View: api_keys."""
    context = build_page_context(request, "subscriptions", "api_keys")
    context["page_title"] = "Api Keys"
    try:
        return render(request, "subscriptions/api_keys.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def api_key_create(request, *args, **kwargs):
    """View: api_key_create."""
    context = build_page_context(request, "subscriptions", "api_key_create")
    context["page_title"] = "Api Key Create"
    try:
        return render(request, "subscriptions/api_key_create.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def bulk_import(request, *args, **kwargs):
    """View: bulk_import."""
    context = build_page_context(request, "subscriptions", "bulk_import")
    context["page_title"] = "Bulk Import"
    try:
        return render(request, "subscriptions/bulk_import.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

