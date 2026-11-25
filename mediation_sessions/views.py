"""Mediation Sessions views."""
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
def mediation_room(request, *args, **kwargs):
    """View: mediation_room."""
    context = build_page_context(request, "mediation_sessions", "mediation_room")
    context["page_title"] = "Mediation Room"
    try:
        return render(request, "mediation_sessions/room.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def join_room(request, *args, **kwargs):
    """View: join_room."""
    context = build_page_context(request, "mediation_sessions", "join_room")
    context["page_title"] = "Join Room"
    try:
        return render(request, "mediation_sessions/join.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def room_participants(request, *args, **kwargs):
    """View: room_participants."""
    context = build_page_context(request, "mediation_sessions", "room_participants")
    context["page_title"] = "Room Participants"
    try:
        return render(request, "mediation_sessions/participants.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def session_notes(request, *args, **kwargs):
    """View: session_notes."""
    context = build_page_context(request, "mediation_sessions", "session_notes")
    context["page_title"] = "Session Notes"
    try:
        return render(request, "mediation_sessions/notes.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def private_caucus(request, *args, **kwargs):
    """View: private_caucus."""
    context = build_page_context(request, "mediation_sessions", "private_caucus")
    context["page_title"] = "Private Caucus"
    try:
        return render(request, "mediation_sessions/caucus.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def recording_consent(request, *args, **kwargs):
    """View: recording_consent."""
    context = build_page_context(request, "mediation_sessions", "recording_consent")
    context["page_title"] = "Recording Consent"
    try:
        return render(request, "mediation_sessions/recording_consent.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def close_room(request, *args, **kwargs):
    """View: close_room."""
    context = build_page_context(request, "mediation_sessions", "close_room")
    context["page_title"] = "Close Room"
    try:
        return render(request, "mediation_sessions/close.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

