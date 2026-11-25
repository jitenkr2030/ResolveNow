"""Mediators views."""
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
def mediator_directory(request, *args, **kwargs):
    """View: mediator_directory."""
    context = build_page_context(request, "mediators", "mediator_directory")
    context["page_title"] = "Mediator Directory"
    try:
        return render(request, "mediators/directory.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def mediator_register(request, *args, **kwargs):
    """View: mediator_register."""
    context = build_page_context(request, "mediators", "mediator_register")
    context["page_title"] = "Mediator Register"
    try:
        return render(request, "mediators/register.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def my_mediator_profile(request, *args, **kwargs):
    """View: my_mediator_profile."""
    context = build_page_context(request, "mediators", "my_mediator_profile")
    context["page_title"] = "My Mediator Profile"
    try:
        return render(request, "mediators/my_profile.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def mediator_profile_edit(request, *args, **kwargs):
    """View: mediator_profile_edit."""
    context = build_page_context(request, "mediators", "mediator_profile_edit")
    context["page_title"] = "Mediator Profile Edit"
    try:
        return render(request, "mediators/profile_edit.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def mediator_availability(request, *args, **kwargs):
    """View: mediator_availability."""
    context = build_page_context(request, "mediators", "mediator_availability")
    context["page_title"] = "Mediator Availability"
    try:
        return render(request, "mediators/availability.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def mediator_public_profile(request, *args, **kwargs):
    """View: mediator_public_profile."""
    context = build_page_context(request, "mediators", "mediator_public_profile")
    context["page_title"] = "Mediator Public Profile"
    try:
        return render(request, "mediators/public_profile.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def mediator_admin_list(request, *args, **kwargs):
    """View: mediator_admin_list."""
    context = build_page_context(request, "mediators", "mediator_admin_list")
    context["page_title"] = "Mediator Admin List"
    try:
        return render(request, "mediators/admin_list.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def mediator_approve(request, *args, **kwargs):
    """View: mediator_approve."""
    context = build_page_context(request, "mediators", "mediator_approve")
    context["page_title"] = "Mediator Approve"
    try:
        return render(request, "mediators/approve.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def mediator_suspend(request, *args, **kwargs):
    """View: mediator_suspend."""
    context = build_page_context(request, "mediators", "mediator_suspend")
    context["page_title"] = "Mediator Suspend"
    try:
        return render(request, "mediators/suspend.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def mediator_feedback_submit(request, *args, **kwargs):
    """View: mediator_feedback_submit."""
    context = build_page_context(request, "mediators", "mediator_feedback_submit")
    context["page_title"] = "Mediator Feedback Submit"
    try:
        return render(request, "mediators/feedback_submit.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

