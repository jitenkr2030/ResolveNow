"""User Profiles views."""
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
def user_profile_redirect(request, *args, **kwargs):
    """View: user_profile_redirect."""
    context = build_page_context(request, "user_profiles", "user_profile_redirect")
    context["page_title"] = "User Profile Redirect"
    try:
        return render(request, "user_profiles/redirect.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def user_profile_edit(request, *args, **kwargs):
    """View: user_profile_edit."""
    context = build_page_context(request, "user_profiles", "user_profile_edit")
    context["page_title"] = "User Profile Edit"
    try:
        return render(request, "user_profiles/edit.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def profile_completion(request, *args, **kwargs):
    """View: profile_completion."""
    context = build_page_context(request, "user_profiles", "profile_completion")
    context["page_title"] = "Profile Completion"
    try:
        return render(request, "user_profiles/completion.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

