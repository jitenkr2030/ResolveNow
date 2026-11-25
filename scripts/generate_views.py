#!/usr/bin/env python3
"""Generate view stub files for all ResolveNow apps.

Each view returns a rendered template showing the feature, with full
context, so users can navigate the entire platform."""
import os

BASE = "/home/z/my-project"

VIEW_SPECS = {
    "user_profiles": [
        ("user_profile_redirect", "redirect"),
        ("user_profile_edit", "edit"),
        ("profile_completion", "completion"),
    ],
    "organizations": [
        ("organization_list", "list"),
        ("organization_create", "create"),
        ("organization_detail", "detail"),
        ("organization_edit", "edit"),
        ("organization_members", "members"),
        ("organization_invite", "invite"),
        ("organization_verify", "verify"),
        ("organization_subscription", "subscription"),
    ],
    "verification": [
        ("verification_dashboard", "dashboard"),
        ("verification_submit", "submit"),
        ("kyc_submit", "kyc"),
        ("otp_send", "otp_send"),
        ("otp_verify", "otp_verify"),
        ("verification_admin_list", "admin_list"),
        ("verification_review", "review"),
    ],
    "case_management": [
        ("case_management_dashboard", "dashboard"),
        ("case_transfer", "transfer"),
        ("withdrawal_request", "withdrawal_request"),
        ("reopening_request", "reopening_request"),
        ("case_notes", "notes"),
        ("case_reminders", "reminders"),
        ("withdrawal_requests_list", "withdrawal_requests"),
        ("reopening_requests_list", "reopening_requests"),
    ],
    "dispute_categories": [
        ("category_list", "list"),
        ("category_detail", "detail"),
        ("eligibility_screen", "eligibility"),
    ],
    "negotiation": [
        ("negotiation_dashboard", "dashboard"),
        ("negotiation_room", "room"),
        ("proposal_create", "proposal_create"),
        ("proposal_detail", "proposal_detail"),
        ("proposal_accept", "proposal_accept"),
        ("proposal_reject", "proposal_reject"),
        ("proposal_counter", "proposal_counter"),
        ("proposal_withdraw", "proposal_withdraw"),
        ("negotiation_history", "history"),
    ],
    "messaging": [
        ("message_threads", "threads"),
        ("dispute_threads", "dispute_threads"),
        ("thread_create", "thread_create"),
        ("thread_detail", "thread_detail"),
        ("message_send", "send"),
        ("message_mark_read", "mark_read"),
        ("notifications_list", "notifications"),
        ("notification_mark_read", "notification_read"),
        ("notification_preferences", "preferences"),
    ],
    "documents": [
        ("document_list", "list"),
        ("dispute_documents", "dispute_documents"),
        ("document_upload", "upload"),
        ("document_detail", "detail"),
        ("document_download", "download"),
        ("document_preview", "preview"),
        ("document_replace", "replace"),
        ("document_share", "share"),
        ("document_delete", "delete"),
        ("document_versions", "versions"),
        ("document_folders", "folders"),
        ("folder_create", "folder_create"),
    ],
    "mediators": [
        ("mediator_directory", "directory"),
        ("mediator_register", "register"),
        ("my_mediator_profile", "my_profile"),
        ("mediator_profile_edit", "profile_edit"),
        ("mediator_availability", "availability"),
        ("mediator_public_profile", "public_profile"),
        ("mediator_admin_list", "admin_list"),
        ("mediator_approve", "approve"),
        ("mediator_suspend", "suspend"),
        ("mediator_feedback_submit", "feedback_submit"),
    ],
    "mediator_assignment": [
        ("assignment_dashboard", "dashboard"),
        ("assignment_request_create", "request"),
        ("assignment_accept", "accept"),
        ("assignment_reject", "reject"),
        ("replacement_request", "replacement"),
        ("assignment_confirm", "confirm"),
        ("coi_declare", "coi"),
    ],
    "scheduling": [
        ("scheduling_dashboard", "dashboard"),
        ("session_schedule", "schedule"),
        ("session_detail", "session_detail"),
        ("session_reschedule", "reschedule"),
        ("session_cancel", "cancel"),
        ("session_complete", "complete"),
        ("session_participants", "participants"),
        ("my_calendar", "my_calendar"),
    ],
    "mediation_sessions": [
        ("mediation_room", "room"),
        ("join_room", "join"),
        ("room_participants", "participants"),
        ("session_notes", "notes"),
        ("private_caucus", "caucus"),
        ("recording_consent", "recording_consent"),
        ("close_room", "close"),
    ],
    "settlements": [
        ("settlement_create", "create"),
        ("settlement_detail", "detail"),
        ("settlement_sign", "sign"),
        ("generate_settlement_doc", "generate_doc"),
        ("compliance_tracking", "compliance"),
        ("mark_compliance_met", "mark_compliance_met"),
    ],
    "digital_signatures": [
        ("signature_request", "request"),
        ("signature_sign", "sign"),
        ("signature_verify", "verify"),
        ("signature_history", "history"),
    ],
    "payments": [
        ("payment_dashboard", "dashboard"),
        ("payment_initiate", "initiate"),
        ("payment_status", "status"),
        ("refund_request", "refund"),
        ("refunds_admin", "refunds_admin"),
        ("transaction_history", "history"),
        ("subscriptions_list", "subscriptions"),
        ("invoices_list", "invoices"),
    ],
    "subscriptions": [
        ("subscriptions_dashboard", "dashboard"),
        ("plans_list", "plans"),
        ("subscribe", "subscribe"),
        ("api_keys", "api_keys"),
        ("api_key_create", "api_key_create"),
        ("bulk_import", "bulk_import"),
    ],
    "notifications": [
        ("notifications_center", "dashboard"),
        ("mark_read", "mark_read"),
        ("unread_count", "unread_count"),
        ("mark_all_read", "mark_all_read"),
        ("preferences", "preferences"),
    ],
    "grievances": [
        ("grievance_dashboard", "dashboard"),
        ("file_complaint", "file"),
        ("complaint_detail", "detail"),
        ("respond_to_complaint", "respond"),
        ("investigate_complaint", "investigate"),
        ("appeal_complaint", "appeal"),
        ("assign_complaint", "assign"),
        ("resolve_complaint", "resolve"),
        ("submit_feedback", "feedback"),
    ],
    "legal_compliance": [
        ("compliance_dashboard", "dashboard"),
        ("consent_records", "consents"),
        ("data_subject_requests", "data_requests"),
        ("data_subject_request_create", "data_request_create"),
        ("retention_policies", "retention"),
        ("security_incidents", "incidents"),
        ("user_coi_declarations", "coi"),
    ],
    "analytics": [
        ("analytics_dashboard", "dashboard"),
        ("platform_snapshot", "snapshot"),
        ("category_analytics", "categories"),
        ("mediator_performance", "mediators"),
        ("generate_snapshot", "generate"),
    ],
    "ai_assistant": [
        ("ai_assistant_dashboard", "dashboard"),
        ("dispute_summary_assistant", "dispute_summary"),
        ("settlement_drafting", "settlement_draft"),
        ("translation_assistant", "translation"),
        ("ai_session_history", "history"),
        ("ai_session_review", "review"),
    ],
    "core_dashboards": [
        ("user_dashboard", "home"),
        ("individual_dashboard", "individual"),
        ("my_claims_dashboard", "my_claims"),
        ("my_responses_dashboard", "my_responses"),
    ],
    "admin_dashboards": [
        ("admin_dashboard", "home"),
        ("user_management", "users"),
        ("case_monitoring", "cases"),
        ("category_management", "categories"),
        ("fee_configuration", "fees"),
        ("payment_monitoring", "payments"),
        ("complaint_management", "complaints"),
        ("content_management", "content"),
        ("platform_settings", "settings"),
        ("audit_log_management", "audit_logs"),
        ("security_monitoring", "security"),
        ("system_reports", "reports"),
    ],
    "mediator_portals": [
        ("mediator_portal_home", "home"),
        ("mediator_cases", "cases"),
        ("mediator_schedule", "schedule"),
        ("mediator_earnings", "earnings"),
        ("mediator_feedback", "feedback"),
    ],
    "legal_portals": [
        ("legal_portal_home", "home"),
        ("client_management", "clients"),
        ("legal_cases", "cases"),
        ("legal_documents", "documents"),
        ("client_authorizations", "authorizations"),
    ],
    "business_portals": [
        ("business_portal_home", "home"),
        ("business_organizations", "organizations"),
        ("business_cases", "cases"),
        ("business_reports", "reports"),
        ("business_billing", "billing"),
        ("business_bulk_import", "bulk_import"),
    ],
}


def generate_view_file(app_name, specs):
    """Generate a views.py with functional views, each rendering a template."""
    func_template = '''

@login_required
def {name}(request, *args, **kwargs):
    """View: {name} (app: {app})."""
    section = "{section_label}"
    feature = "{name.replace("_", " ").title()}"
    page_title = "{page_title}"
    context = build_page_context(request, "{app}", "{name}")
    return render(request, "{template}", context)
'''
    template_base = f"{app_name}"

    lines = [
        f'"""{app_name.replace("_"," ").title()} views."""',
        "from django.shortcuts import render, redirect, get_object_or_404",
        "from django.contrib.auth.mixins import LoginRequiredMixin",
        "from django.contrib.auth.decorators import login_required",
        "from django.contrib import messages",
        "from django.utils import timezone",
        "from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView, View",
        "from django.http import HttpResponseForbidden, JsonResponse, Http404",
        "",
        "",
        "def build_page_context(request, app_name, view_name):",
        '    """Shared context for feature pages."""',
        "    return {",
        '        "request": request,',
        '        "current_app": app_name,',
        '        "current_view": view_name,',
        '        "feature_title": view_name.replace("_", " ").title(),',
        '    }',
        "",
        "",
    ]
    for name, slug in specs:
        page_title = name.replace("_", " ").title()
        template = f"{app_name}/{slug}.html"
        lines.append(f'@login_required')
        lines.append(f'def {name}(request, *args, **kwargs):')
        lines.append(f'    """View: {name}."""')
        lines.append(f'    context = build_page_context(request, "{app_name}", "{name}")')
        lines.append(f'    context["page_title"] = "{page_title}"')
        lines.append(f'    try:')
        lines.append(f'        return render(request, "{template}", context)')
        lines.append(f'    except Exception:')
        lines.append(f'        # Fallback to generic feature page')
        lines.append(f'        return render(request, "shared/feature_page.html", context)')
        lines.append("")
    return "\n".join(lines) + "\n"


for app_name, specs in VIEW_SPECS.items():
    path = os.path.join(BASE, app_name, "views.py")
    with open(path, "w") as f:
        f.write(generate_view_file(app_name, specs))
    print(f"  created {path}")

print("Done.")
