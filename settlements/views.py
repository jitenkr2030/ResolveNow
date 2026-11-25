"""Settlements views."""
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
def settlement_create(request, *args, **kwargs):
    """View: settlement_create."""
    context = build_page_context(request, "settlements", "settlement_create")
    context["page_title"] = "Settlement Create"
    try:
        return render(request, "settlements/create.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def settlement_detail(request, *args, **kwargs):
    """View: settlement_detail."""
    context = build_page_context(request, "settlements", "settlement_detail")
    context["page_title"] = "Settlement Detail"
    try:
        return render(request, "settlements/detail.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def settlement_sign(request, *args, **kwargs):
    """View: settlement_sign."""
    context = build_page_context(request, "settlements", "settlement_sign")
    context["page_title"] = "Settlement Sign"
    try:
        return render(request, "settlements/sign.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def generate_settlement_doc(request, *args, **kwargs):
    """View: generate_settlement_doc."""
    context = build_page_context(request, "settlements", "generate_settlement_doc")
    context["page_title"] = "Generate Settlement Doc"
    try:
        return render(request, "settlements/generate_doc.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def compliance_tracking(request, *args, **kwargs):
    """View: compliance_tracking."""
    context = build_page_context(request, "settlements", "compliance_tracking")
    context["page_title"] = "Compliance Tracking"
    try:
        return render(request, "settlements/compliance.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def mark_compliance_met(request, *args, **kwargs):
    """View: mark_compliance_met."""
    context = build_page_context(request, "settlements", "mark_compliance_met")
    context["page_title"] = "Mark Compliance Met"
    try:
        return render(request, "settlements/mark_compliance_met.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

