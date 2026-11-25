"""Legal Portals views."""
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
def legal_portal_home(request, *args, **kwargs):
    """View: legal_portal_home."""
    context = build_page_context(request, "legal_portals", "legal_portal_home")
    context["page_title"] = "Legal Portal Home"
    try:
        return render(request, "legal_portals/home.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def client_management(request, *args, **kwargs):
    """View: client_management."""
    context = build_page_context(request, "legal_portals", "client_management")
    context["page_title"] = "Client Management"
    try:
        return render(request, "legal_portals/clients.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def legal_cases(request, *args, **kwargs):
    """View: legal_cases."""
    context = build_page_context(request, "legal_portals", "legal_cases")
    context["page_title"] = "Legal Cases"
    try:
        return render(request, "legal_portals/cases.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def legal_documents(request, *args, **kwargs):
    """View: legal_documents."""
    context = build_page_context(request, "legal_portals", "legal_documents")
    context["page_title"] = "Legal Documents"
    try:
        return render(request, "legal_portals/documents.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def client_authorizations(request, *args, **kwargs):
    """View: client_authorizations."""
    context = build_page_context(request, "legal_portals", "client_authorizations")
    context["page_title"] = "Client Authorizations"
    try:
        return render(request, "legal_portals/authorizations.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

