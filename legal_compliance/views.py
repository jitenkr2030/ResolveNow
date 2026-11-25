"""Legal Compliance views."""
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
def compliance_dashboard(request, *args, **kwargs):
    """View: compliance_dashboard."""
    context = build_page_context(request, "legal_compliance", "compliance_dashboard")
    context["page_title"] = "Compliance Dashboard"
    try:
        return render(request, "legal_compliance/dashboard.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def consent_records(request, *args, **kwargs):
    """View: consent_records."""
    context = build_page_context(request, "legal_compliance", "consent_records")
    context["page_title"] = "Consent Records"
    try:
        return render(request, "legal_compliance/consents.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def data_subject_requests(request, *args, **kwargs):
    """View: data_subject_requests."""
    context = build_page_context(request, "legal_compliance", "data_subject_requests")
    context["page_title"] = "Data Subject Requests"
    try:
        return render(request, "legal_compliance/data_requests.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def data_subject_request_create(request, *args, **kwargs):
    """View: data_subject_request_create."""
    context = build_page_context(request, "legal_compliance", "data_subject_request_create")
    context["page_title"] = "Data Subject Request Create"
    try:
        return render(request, "legal_compliance/data_request_create.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def retention_policies(request, *args, **kwargs):
    """View: retention_policies."""
    context = build_page_context(request, "legal_compliance", "retention_policies")
    context["page_title"] = "Retention Policies"
    try:
        return render(request, "legal_compliance/retention.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def security_incidents(request, *args, **kwargs):
    """View: security_incidents."""
    context = build_page_context(request, "legal_compliance", "security_incidents")
    context["page_title"] = "Security Incidents"
    try:
        return render(request, "legal_compliance/incidents.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def user_coi_declarations(request, *args, **kwargs):
    """View: user_coi_declarations."""
    context = build_page_context(request, "legal_compliance", "user_coi_declarations")
    context["page_title"] = "User Coi Declarations"
    try:
        return render(request, "legal_compliance/coi.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

