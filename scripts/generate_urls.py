#!/usr/bin/env python3
"""Generate URL files for all ResolveNow apps with comprehensive endpoints."""
import os

BASE = "/home/z/my-project"

APP_URLS = {
    "user_profiles": [
        ("", "user_profile_redirect", "dashboard"),
        ("edit/", "user_profile_edit", "edit"),
        ("completion/", "profile_completion", "completion"),
    ],
    "organizations": [
        ("", "organization_list", "list"),
        ("create/", "organization_create", "create"),
        ("<int:pk>/", "organization_detail", "detail"),
        ("<int:pk>/edit/", "organization_edit", "edit"),
        ("<int:pk>/members/", "organization_members", "members"),
        ("<int:pk>/invite/", "organization_invite", "invite"),
        ("<int:pk>/verify/", "organization_verify", "verify"),
        ("<int:pk>/subscription/", "organization_subscription", "subscription"),
    ],
    "verification": [
        ("", "verification_dashboard", "dashboard"),
        ("submit/", "verification_submit", "submit"),
        ("kyc/", "kyc_submit", "kyc"),
        ("otp/send/", "otp_send", "otp_send"),
        ("otp/verify/", "otp_verify", "otp_verify"),
        ("admin/", "verification_admin_list", "admin_list"),
        ("<int:pk>/review/", "verification_review", "review"),
    ],
    "disputes": [
        ("", "dispute_list", "list"),
        ("create/", "dispute_create", "create"),
        ("draft/", "dispute_draft_list", "drafts"),
        ("<int:pk>/", "dispute_detail", "detail"),
        ("<int:pk>/edit/", "dispute_edit", "edit"),
        ("<int:pk>/submit/", "dispute_submit", "submit"),
        ("<int:pk>/withdraw/", "dispute_withdraw", "withdraw"),
        ("<int:pk>/timeline/", "dispute_timeline", "timeline"),
        ("<int:pk>/parties/", "dispute_parties", "parties"),
        ("<int:pk>/invite-party/", "invite_party", "invite_party"),
        ("<int:pk>/accept-invite/<token>/", "accept_invitation", "accept_invitation"),
        ("<int:pk>/eligibility/", "dispute_eligibility", "eligibility"),
        ("<int:pk>/change-status/", "change_status", "change_status"),
        ("<int:pk>/assign-manager/", "assign_case_manager", "assign_manager"),
        ("<int:pk>/close/", "dispute_close", "close"),
        ("<int:pk>/reopen/", "dispute_reopen", "reopen"),
        ("<int:pk>/archive/", "dispute_archive", "archive"),
        ("track/", "track_application_status", "track_status"),
    ],
    "case_management": [
        ("", "case_management_dashboard", "dashboard"),
        ("<int:dispute_id>/transfer/", "case_transfer", "transfer"),
        ("<int:dispute_id>/withdrawal-request/", "withdrawal_request", "withdrawal_request"),
        ("<int:dispute_id>/reopening-request/", "reopening_request", "reopening_request"),
        ("<int:dispute_id>/notes/", "case_notes", "notes"),
        ("<int:dispute_id>/reminders/", "case_reminders", "reminders"),
        ("withdrawal-requests/", "withdrawal_requests_list", "withdrawal_requests"),
        ("reopening-requests/", "reopening_requests_list", "reopening_requests"),
    ],
    "dispute_categories": [
        ("", "category_list", "list"),
        ("<slug:slug>/", "category_detail", "detail"),
        ("<slug:slug>/eligibility/", "eligibility_screen", "eligibility"),
    ],
    "negotiation": [
        ("", "negotiation_dashboard", "dashboard"),
        ("<int:dispute_id>/room/", "negotiation_room", "room"),
        ("<int:dispute_id>/proposal/create/", "proposal_create", "proposal_create"),
        ("<int:proposal_id>/", "proposal_detail", "proposal_detail"),
        ("<int:proposal_id>/accept/", "proposal_accept", "proposal_accept"),
        ("<int:proposal_id>/reject/", "proposal_reject", "proposal_reject"),
        ("<int:proposal_id>/counter/", "proposal_counter", "proposal_counter"),
        ("<int:proposal_id>/withdraw/", "proposal_withdraw", "proposal_withdraw"),
        ("<int:dispute_id>/history/", "negotiation_history", "history"),
    ],
    "messaging": [
        ("", "message_threads", "threads"),
        ("<int:dispute_id>/threads/", "dispute_threads", "dispute_threads"),
        ("<int:dispute_id>/thread/create/", "thread_create", "thread_create"),
        ("<int:thread_id>/", "thread_detail", "thread_detail"),
        ("<int:thread_id>/send/", "message_send", "send"),
        ("<int:message_id>/read/", "message_mark_read", "mark_read"),
        ("notifications/", "notifications_list", "notifications"),
        ("notifications/<int:notif_id>/read/", "notification_mark_read", "notification_read"),
        ("preferences/", "notification_preferences", "preferences"),
    ],
    "documents": [
        ("", "document_list", "list"),
        ("<int:dispute_id>/", "dispute_documents", "dispute_documents"),
        ("<int:dispute_id>/upload/", "document_upload", "upload"),
        ("<int:pk>/", "document_detail", "detail"),
        ("<int:pk>/download/", "document_download", "download"),
        ("<int:pk>/preview/", "document_preview", "preview"),
        ("<int:pk>/replace/", "document_replace", "replace"),
        ("<int:pk>/share/", "document_share", "share"),
        ("<int:pk>/delete/", "document_delete", "delete"),
        ("<int:pk>/versions/", "document_versions", "versions"),
        ("<int:dispute_id>/folders/", "document_folders", "folders"),
        ("<int:dispute_id>/folders/create/", "folder_create", "folder_create"),
    ],
    "mediators": [
        ("", "mediator_directory", "directory"),
        ("register/", "mediator_register", "register"),
        ("profile/", "my_mediator_profile", "my_profile"),
        ("profile/edit/", "mediator_profile_edit", "profile_edit"),
        ("availability/", "mediator_availability", "availability"),
        ("<int:pk>/", "mediator_public_profile", "public_profile"),
        ("admin/", "mediator_admin_list", "admin_list"),
        ("<int:pk>/approve/", "mediator_approve", "approve"),
        ("<int:pk>/suspend/", "mediator_suspend", "suspend"),
        ("<int:pk>/feedback/", "mediator_feedback_submit", "feedback_submit"),
    ],
    "mediator_assignment": [
        ("", "assignment_dashboard", "dashboard"),
        ("<int:dispute_id>/request/", "assignment_request_create", "request"),
        ("<int:request_id>/accept/", "assignment_accept", "accept"),
        ("<int:request_id>/reject/", "assignment_reject", "reject"),
        ("<int:dispute_id>/replacement/", "replacement_request", "replacement"),
        ("<int:request_id>/confirm/", "assignment_confirm", "confirm"),
        ("coi/<int:dispute_id>/", "coi_declare", "coi"),
    ],
    "scheduling": [
        ("", "scheduling_dashboard", "dashboard"),
        ("<int:dispute_id>/schedule/", "session_schedule", "schedule"),
        ("<int:session_id>/", "session_detail", "session_detail"),
        ("<int:session_id>/reschedule/", "session_reschedule", "reschedule"),
        ("<int:session_id>/cancel/", "session_cancel", "cancel"),
        ("<int:session_id>/complete/", "session_complete", "complete"),
        ("<int:session_id>/participants/", "session_participants", "participants"),
        ("my-calendar/", "my_calendar", "my_calendar"),
    ],
    "mediation_sessions": [
        ("<int:session_id>/room/", "mediation_room", "room"),
        ("<int:session_id>/join/", "join_room", "join"),
        ("<int:room_id>/participants/", "room_participants", "participants"),
        ("<int:room_id>/notes/", "session_notes", "notes"),
        ("<int:room_id>/caucus/", "private_caucus", "caucus"),
        ("<int:room_id>/recording-consent/", "recording_consent", "recording_consent"),
        ("<int:room_id>/close/", "close_room", "close"),
    ],
    "settlements": [
        ("<int:dispute_id>/create/", "settlement_create", "create"),
        ("<int:pk>/", "settlement_detail", "detail"),
        ("<int:pk>/sign/", "settlement_sign", "sign"),
        ("<int:pk>/generate-doc/", "generate_settlement_doc", "generate_doc"),
        ("<int:pk>/compliance/", "compliance_tracking", "compliance"),
        ("<int:compliance_id>/mark-met/", "mark_compliance_met", "mark_compliance_met"),
    ],
    "digital_signatures": [
        ("request/", "signature_request", "request"),
        ("<int:pk>/sign/", "signature_sign", "sign"),
        ("<int:pk>/verify/", "signature_verify", "verify"),
        ("history/", "signature_history", "history"),
    ],
    "payments": [
        ("", "payment_dashboard", "dashboard"),
        ("<int:dispute_id>/pay/", "payment_initiate", "initiate"),
        ("<int:pk>/status/", "payment_status", "status"),
        ("<int:pk>/refund/", "refund_request", "refund"),
        ("refunds/", "refunds_admin", "refunds_admin"),
        ("history/", "transaction_history", "history"),
        ("subscriptions/", "subscriptions_list", "subscriptions"),
        ("invoices/", "invoices_list", "invoices"),
    ],
    "subscriptions": [
        ("", "subscriptions_dashboard", "dashboard"),
        ("plans/", "plans_list", "plans"),
        ("subscribe/<int:plan_id>/", "subscribe", "subscribe"),
        ("api-keys/", "api_keys", "api_keys"),
        ("api-keys/create/", "api_key_create", "api_key_create"),
        ("bulk-import/", "bulk_import", "bulk_import"),
    ],
    "notifications": [
        ("", "notifications_center", "dashboard"),
        ("<int:pk>/read/", "mark_read", "mark_read"),
        ("unread/", "unread_count", "unread_count"),
        ("mark-all-read/", "mark_all_read", "mark_all_read"),
        ("preferences/", "preferences", "preferences"),
    ],
    "grievances": [
        ("", "grievance_dashboard", "dashboard"),
        ("file/", "file_complaint", "file"),
        ("<int:pk>/", "complaint_detail", "detail"),
        ("<int:pk>/respond/", "respond_to_complaint", "respond"),
        ("<int:pk>/investigate/", "investigate_complaint", "investigate"),
        ("<int:pk>/appeal/", "appeal_complaint", "appeal"),
        ("<int:pk>/assign/", "assign_complaint", "assign"),
        ("<int:pk>/resolve/", "resolve_complaint", "resolve"),
        ("feedback/", "submit_feedback", "feedback"),
    ],
    "legal_compliance": [
        ("", "compliance_dashboard", "dashboard"),
        ("consents/", "consent_records", "consents"),
        ("data-requests/", "data_subject_requests", "data_requests"),
        ("data-requests/create/", "data_subject_request_create", "data_request_create"),
        ("retention-policies/", "retention_policies", "retention"),
        ("incidents/", "security_incidents", "incidents"),
        ("coi/", "user_coi_declarations", "coi"),
    ],
    "analytics": [
        ("", "analytics_dashboard", "dashboard"),
        ("snapshot/", "platform_snapshot", "snapshot"),
        ("categories/", "category_analytics", "categories"),
        ("mediators/", "mediator_performance", "mediators"),
        ("generate/", "generate_snapshot", "generate"),
    ],
    "ai_assistant": [
        ("", "ai_assistant_dashboard", "dashboard"),
        ("dispute-summary/", "dispute_summary_assistant", "dispute_summary"),
        ("settlement-draft/", "settlement_drafting", "settlement_draft"),
        ("translation/", "translation_assistant", "translation"),
        ("history/", "ai_session_history", "history"),
        ("<int:session_id>/review/", "ai_session_review", "review"),
    ],
    "core_dashboards": [
        ("", "user_dashboard", "home"),
        ("individual/", "individual_dashboard", "individual"),
        ("claims/", "my_claims_dashboard", "my_claims"),
        ("responses/", "my_responses_dashboard", "my_responses"),
    ],
    "admin_dashboards": [
        ("", "admin_dashboard", "home"),
        ("users/", "user_management", "users"),
        ("cases/", "case_monitoring", "cases"),
        ("categories/", "category_management", "categories"),
        ("fees/", "fee_configuration", "fees"),
        ("payments/", "payment_monitoring", "payments"),
        ("complaints/", "complaint_management", "complaints"),
        ("content/", "content_management", "content"),
        ("settings/", "platform_settings", "settings"),
        ("audit-logs/", "audit_log_management", "audit_logs"),
        ("security/", "security_monitoring", "security"),
        ("reports/", "system_reports", "reports"),
    ],
    "mediator_portals": [
        ("", "mediator_portal_home", "home"),
        ("cases/", "mediator_cases", "cases"),
        ("schedule/", "mediator_schedule", "schedule"),
        ("earnings/", "mediator_earnings", "earnings"),
        ("feedback/", "mediator_feedback", "feedback"),
    ],
    "legal_portals": [
        ("", "legal_portal_home", "home"),
        ("clients/", "client_management", "clients"),
        ("cases/", "legal_cases", "cases"),
        ("documents/", "legal_documents", "documents"),
        ("authorizations/", "client_authorizations", "authorizations"),
    ],
    "business_portals": [
        ("", "business_portal_home", "home"),
        ("organizations/", "business_organizations", "organizations"),
        ("cases/", "business_cases", "cases"),
        ("reports/", "business_reports", "reports"),
        ("billing/", "business_billing", "billing"),
        ("bulk-import/", "business_bulk_import", "bulk_import"),
    ],
}

NAMESPACE_MAP = {
    "dispute_categories": "categories",
    "core_dashboards": "dashboard",
    "admin_dashboards": "admin_dash",
    "mediator_portals": "mediator_portal",
    "legal_portals": "legal_portal",
    "business_portals": "business_portal",
}


def generate_urls_file(app_name, patterns):
    view_module = f"{app_name}.views"
    namespace = NAMESPACE_MAP.get(app_name, app_name)
    lines = [
        f"from django.urls import path",
        f"from {view_module} import *",
        "",
        f"app_name = \"{namespace}\"",
        "",
        "urlpatterns = [",
    ]
    for pattern, view_name, url_name in patterns:
        lines.append(f'    path("{pattern}", {view_name}, name="{url_name}"),')
    lines.append("]")
    return "\n".join(lines) + "\n"


for app_name, patterns in APP_URLS.items():
    url_path = os.path.join(BASE, app_name, "urls.py")
    content = generate_urls_file(app_name, patterns)
    with open(url_path, "w") as f:
        f.write(content)
    print(f"  created {url_path}")

print("Done.")
