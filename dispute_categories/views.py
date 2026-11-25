"""Dispute Categories views."""
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
def category_list(request, *args, **kwargs):
    """View: category_list."""
    context = build_page_context(request, "dispute_categories", "category_list")
    context["page_title"] = "Category List"
    try:
        return render(request, "dispute_categories/list.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def category_detail(request, *args, **kwargs):
    """View: category_detail."""
    context = build_page_context(request, "dispute_categories", "category_detail")
    context["page_title"] = "Category Detail"
    try:
        return render(request, "dispute_categories/detail.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def eligibility_screen(request, *args, **kwargs):
    """View: eligibility_screen."""
    context = build_page_context(request, "dispute_categories", "eligibility_screen")
    context["page_title"] = "Eligibility Screen"
    try:
        return render(request, "dispute_categories/eligibility.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

