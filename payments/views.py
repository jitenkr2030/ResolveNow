"""Payments views."""
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
def payment_dashboard(request, *args, **kwargs):
    """View: payment_dashboard."""
    context = build_page_context(request, "payments", "payment_dashboard")
    context["page_title"] = "Payment Dashboard"
    try:
        return render(request, "payments/dashboard.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def payment_initiate(request, *args, **kwargs):
    """View: payment_initiate."""
    context = build_page_context(request, "payments", "payment_initiate")
    context["page_title"] = "Payment Initiate"
    try:
        return render(request, "payments/initiate.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def payment_status(request, *args, **kwargs):
    """View: payment_status."""
    context = build_page_context(request, "payments", "payment_status")
    context["page_title"] = "Payment Status"
    try:
        return render(request, "payments/status.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def refund_request(request, *args, **kwargs):
    """View: refund_request."""
    context = build_page_context(request, "payments", "refund_request")
    context["page_title"] = "Refund Request"
    try:
        return render(request, "payments/refund.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def refunds_admin(request, *args, **kwargs):
    """View: refunds_admin."""
    context = build_page_context(request, "payments", "refunds_admin")
    context["page_title"] = "Refunds Admin"
    try:
        return render(request, "payments/refunds_admin.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def transaction_history(request, *args, **kwargs):
    """View: transaction_history."""
    context = build_page_context(request, "payments", "transaction_history")
    context["page_title"] = "Transaction History"
    try:
        return render(request, "payments/history.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def subscriptions_list(request, *args, **kwargs):
    """View: subscriptions_list."""
    context = build_page_context(request, "payments", "subscriptions_list")
    context["page_title"] = "Subscriptions List"
    try:
        return render(request, "payments/subscriptions.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def invoices_list(request, *args, **kwargs):
    """View: invoices_list."""
    context = build_page_context(request, "payments", "invoices_list")
    context["page_title"] = "Invoices List"
    try:
        return render(request, "payments/invoices.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

