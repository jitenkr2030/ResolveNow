"""Business Portals views."""
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
def business_portal_home(request, *args, **kwargs):
    """View: business_portal_home."""
    context = build_page_context(request, "business_portals", "business_portal_home")
    context["page_title"] = "Business Portal Home"
    try:
        return render(request, "business_portals/home.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def business_organizations(request, *args, **kwargs):
    """View: business_organizations."""
    context = build_page_context(request, "business_portals", "business_organizations")
    context["page_title"] = "Business Organizations"
    try:
        return render(request, "business_portals/organizations.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def business_cases(request, *args, **kwargs):
    """View: business_cases."""
    context = build_page_context(request, "business_portals", "business_cases")
    context["page_title"] = "Business Cases"
    try:
        return render(request, "business_portals/cases.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def business_reports(request, *args, **kwargs):
    """View: business_reports."""
    context = build_page_context(request, "business_portals", "business_reports")
    context["page_title"] = "Business Reports"
    try:
        return render(request, "business_portals/reports.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def business_billing(request, *args, **kwargs):
    """View: business_billing."""
    context = build_page_context(request, "business_portals", "business_billing")
    context["page_title"] = "Business Billing"
    try:
        return render(request, "business_portals/billing.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def business_bulk_import(request, *args, **kwargs):
    """View: business_bulk_import."""
    context = build_page_context(request, "business_portals", "business_bulk_import")
    context["page_title"] = "Business Bulk Import"
    try:
        return render(request, "business_portals/bulk_import.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

