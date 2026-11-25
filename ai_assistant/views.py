"""Ai Assistant views."""
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
def ai_assistant_dashboard(request, *args, **kwargs):
    """View: ai_assistant_dashboard."""
    context = build_page_context(request, "ai_assistant", "ai_assistant_dashboard")
    context["page_title"] = "Ai Assistant Dashboard"
    try:
        return render(request, "ai_assistant/dashboard.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def dispute_summary_assistant(request, *args, **kwargs):
    """View: dispute_summary_assistant."""
    context = build_page_context(request, "ai_assistant", "dispute_summary_assistant")
    context["page_title"] = "Dispute Summary Assistant"
    try:
        return render(request, "ai_assistant/dispute_summary.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def settlement_drafting(request, *args, **kwargs):
    """View: settlement_drafting."""
    context = build_page_context(request, "ai_assistant", "settlement_drafting")
    context["page_title"] = "Settlement Drafting"
    try:
        return render(request, "ai_assistant/settlement_draft.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def translation_assistant(request, *args, **kwargs):
    """View: translation_assistant."""
    context = build_page_context(request, "ai_assistant", "translation_assistant")
    context["page_title"] = "Translation Assistant"
    try:
        return render(request, "ai_assistant/translation.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def ai_session_history(request, *args, **kwargs):
    """View: ai_session_history."""
    context = build_page_context(request, "ai_assistant", "ai_session_history")
    context["page_title"] = "Ai Session History"
    try:
        return render(request, "ai_assistant/history.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def ai_session_review(request, *args, **kwargs):
    """View: ai_session_review."""
    context = build_page_context(request, "ai_assistant", "ai_session_review")
    context["page_title"] = "Ai Session Review"
    try:
        return render(request, "ai_assistant/review.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

