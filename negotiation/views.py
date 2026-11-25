"""Negotiation views."""
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
def negotiation_dashboard(request, *args, **kwargs):
    """View: negotiation_dashboard."""
    context = build_page_context(request, "negotiation", "negotiation_dashboard")
    context["page_title"] = "Negotiation Dashboard"
    try:
        return render(request, "negotiation/dashboard.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def negotiation_room(request, *args, **kwargs):
    """View: negotiation_room."""
    context = build_page_context(request, "negotiation", "negotiation_room")
    context["page_title"] = "Negotiation Room"
    try:
        return render(request, "negotiation/room.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def proposal_create(request, *args, **kwargs):
    """View: proposal_create."""
    context = build_page_context(request, "negotiation", "proposal_create")
    context["page_title"] = "Proposal Create"
    try:
        return render(request, "negotiation/proposal_create.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def proposal_detail(request, *args, **kwargs):
    """View: proposal_detail."""
    context = build_page_context(request, "negotiation", "proposal_detail")
    context["page_title"] = "Proposal Detail"
    try:
        return render(request, "negotiation/proposal_detail.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def proposal_accept(request, *args, **kwargs):
    """View: proposal_accept."""
    context = build_page_context(request, "negotiation", "proposal_accept")
    context["page_title"] = "Proposal Accept"
    try:
        return render(request, "negotiation/proposal_accept.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def proposal_reject(request, *args, **kwargs):
    """View: proposal_reject."""
    context = build_page_context(request, "negotiation", "proposal_reject")
    context["page_title"] = "Proposal Reject"
    try:
        return render(request, "negotiation/proposal_reject.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def proposal_counter(request, *args, **kwargs):
    """View: proposal_counter."""
    context = build_page_context(request, "negotiation", "proposal_counter")
    context["page_title"] = "Proposal Counter"
    try:
        return render(request, "negotiation/proposal_counter.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def proposal_withdraw(request, *args, **kwargs):
    """View: proposal_withdraw."""
    context = build_page_context(request, "negotiation", "proposal_withdraw")
    context["page_title"] = "Proposal Withdraw"
    try:
        return render(request, "negotiation/proposal_withdraw.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def negotiation_history(request, *args, **kwargs):
    """View: negotiation_history."""
    context = build_page_context(request, "negotiation", "negotiation_history")
    context["page_title"] = "Negotiation History"
    try:
        return render(request, "negotiation/history.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

