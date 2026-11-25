"""Verification views."""
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
def verification_dashboard(request, *args, **kwargs):
    """View: verification_dashboard."""
    context = build_page_context(request, "verification", "verification_dashboard")
    context["page_title"] = "Verification Dashboard"
    try:
        return render(request, "verification/dashboard.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def verification_submit(request, *args, **kwargs):
    """View: verification_submit."""
    context = build_page_context(request, "verification", "verification_submit")
    context["page_title"] = "Verification Submit"
    try:
        return render(request, "verification/submit.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def kyc_submit(request, *args, **kwargs):
    """View: kyc_submit."""
    context = build_page_context(request, "verification", "kyc_submit")
    context["page_title"] = "Kyc Submit"
    try:
        return render(request, "verification/kyc.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def otp_send(request, *args, **kwargs):
    """View: otp_send."""
    context = build_page_context(request, "verification", "otp_send")
    context["page_title"] = "Otp Send"
    try:
        return render(request, "verification/otp_send.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def otp_verify(request, *args, **kwargs):
    """View: otp_verify."""
    context = build_page_context(request, "verification", "otp_verify")
    context["page_title"] = "Otp Verify"
    try:
        return render(request, "verification/otp_verify.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def verification_admin_list(request, *args, **kwargs):
    """View: verification_admin_list."""
    context = build_page_context(request, "verification", "verification_admin_list")
    context["page_title"] = "Verification Admin List"
    try:
        return render(request, "verification/admin_list.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def verification_review(request, *args, **kwargs):
    """View: verification_review."""
    context = build_page_context(request, "verification", "verification_review")
    context["page_title"] = "Verification Review"
    try:
        return render(request, "verification/review.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

