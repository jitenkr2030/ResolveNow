"""Notifications views."""
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
def notifications_center(request, *args, **kwargs):
    """View: notifications_center."""
    context = build_page_context(request, "notifications", "notifications_center")
    context["page_title"] = "Notifications Center"
    try:
        return render(request, "notifications/dashboard.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def mark_read(request, *args, **kwargs):
    """View: mark_read."""
    context = build_page_context(request, "notifications", "mark_read")
    context["page_title"] = "Mark Read"
    try:
        return render(request, "notifications/mark_read.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def unread_count(request, *args, **kwargs):
    """View: unread_count."""
    context = build_page_context(request, "notifications", "unread_count")
    context["page_title"] = "Unread Count"
    try:
        return render(request, "notifications/unread_count.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def mark_all_read(request, *args, **kwargs):
    """View: mark_all_read."""
    context = build_page_context(request, "notifications", "mark_all_read")
    context["page_title"] = "Mark All Read"
    try:
        return render(request, "notifications/mark_all_read.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def preferences(request, *args, **kwargs):
    """View: preferences."""
    context = build_page_context(request, "notifications", "preferences")
    context["page_title"] = "Preferences"
    try:
        return render(request, "notifications/preferences.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

