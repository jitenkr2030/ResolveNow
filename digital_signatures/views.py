"""Digital Signatures views."""
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
def signature_request(request, *args, **kwargs):
    """View: signature_request."""
    context = build_page_context(request, "digital_signatures", "signature_request")
    context["page_title"] = "Signature Request"
    try:
        return render(request, "digital_signatures/request.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def signature_sign(request, *args, **kwargs):
    """View: signature_sign."""
    context = build_page_context(request, "digital_signatures", "signature_sign")
    context["page_title"] = "Signature Sign"
    try:
        return render(request, "digital_signatures/sign.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def signature_verify(request, *args, **kwargs):
    """View: signature_verify."""
    context = build_page_context(request, "digital_signatures", "signature_verify")
    context["page_title"] = "Signature Verify"
    try:
        return render(request, "digital_signatures/verify.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def signature_history(request, *args, **kwargs):
    """View: signature_history."""
    context = build_page_context(request, "digital_signatures", "signature_history")
    context["page_title"] = "Signature History"
    try:
        return render(request, "digital_signatures/history.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

