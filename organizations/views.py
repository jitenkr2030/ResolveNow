"""Organizations views."""
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
def organization_list(request, *args, **kwargs):
    """View: organization_list."""
    context = build_page_context(request, "organizations", "organization_list")
    context["page_title"] = "Organization List"
    try:
        return render(request, "organizations/list.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def organization_create(request, *args, **kwargs):
    """View: organization_create."""
    context = build_page_context(request, "organizations", "organization_create")
    context["page_title"] = "Organization Create"
    try:
        return render(request, "organizations/create.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def organization_detail(request, *args, **kwargs):
    """View: organization_detail."""
    context = build_page_context(request, "organizations", "organization_detail")
    context["page_title"] = "Organization Detail"
    try:
        return render(request, "organizations/detail.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def organization_edit(request, *args, **kwargs):
    """View: organization_edit."""
    context = build_page_context(request, "organizations", "organization_edit")
    context["page_title"] = "Organization Edit"
    try:
        return render(request, "organizations/edit.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def organization_members(request, *args, **kwargs):
    """View: organization_members."""
    context = build_page_context(request, "organizations", "organization_members")
    context["page_title"] = "Organization Members"
    try:
        return render(request, "organizations/members.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def organization_invite(request, *args, **kwargs):
    """View: organization_invite."""
    context = build_page_context(request, "organizations", "organization_invite")
    context["page_title"] = "Organization Invite"
    try:
        return render(request, "organizations/invite.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def organization_verify(request, *args, **kwargs):
    """View: organization_verify."""
    context = build_page_context(request, "organizations", "organization_verify")
    context["page_title"] = "Organization Verify"
    try:
        return render(request, "organizations/verify.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def organization_subscription(request, *args, **kwargs):
    """View: organization_subscription."""
    context = build_page_context(request, "organizations", "organization_subscription")
    context["page_title"] = "Organization Subscription"
    try:
        return render(request, "organizations/subscription.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

