"""Messaging views."""
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
def message_threads(request, *args, **kwargs):
    """View: message_threads."""
    context = build_page_context(request, "messaging", "message_threads")
    context["page_title"] = "Message Threads"
    try:
        return render(request, "messaging/threads.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def dispute_threads(request, *args, **kwargs):
    """View: dispute_threads."""
    context = build_page_context(request, "messaging", "dispute_threads")
    context["page_title"] = "Dispute Threads"
    try:
        return render(request, "messaging/dispute_threads.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def thread_create(request, *args, **kwargs):
    """View: thread_create."""
    context = build_page_context(request, "messaging", "thread_create")
    context["page_title"] = "Thread Create"
    try:
        return render(request, "messaging/thread_create.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def thread_detail(request, *args, **kwargs):
    """View: thread_detail."""
    context = build_page_context(request, "messaging", "thread_detail")
    context["page_title"] = "Thread Detail"
    try:
        return render(request, "messaging/thread_detail.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def message_send(request, *args, **kwargs):
    """View: message_send."""
    context = build_page_context(request, "messaging", "message_send")
    context["page_title"] = "Message Send"
    try:
        return render(request, "messaging/send.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def message_mark_read(request, *args, **kwargs):
    """View: message_mark_read."""
    context = build_page_context(request, "messaging", "message_mark_read")
    context["page_title"] = "Message Mark Read"
    try:
        return render(request, "messaging/mark_read.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def notifications_list(request, *args, **kwargs):
    """View: notifications_list."""
    context = build_page_context(request, "messaging", "notifications_list")
    context["page_title"] = "Notifications List"
    try:
        return render(request, "messaging/notifications.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def notification_mark_read(request, *args, **kwargs):
    """View: notification_mark_read."""
    context = build_page_context(request, "messaging", "notification_mark_read")
    context["page_title"] = "Notification Mark Read"
    try:
        return render(request, "messaging/notification_read.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def notification_preferences(request, *args, **kwargs):
    """View: notification_preferences."""
    context = build_page_context(request, "messaging", "notification_preferences")
    context["page_title"] = "Notification Preferences"
    try:
        return render(request, "messaging/preferences.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

