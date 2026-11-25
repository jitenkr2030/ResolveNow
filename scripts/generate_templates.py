#!/usr/bin/env python3
"""Generate stub HTML templates for all ResolveNow apps."""
import os

BASE = "/home/z/my-project"

TEMPLATE_SPECS = {
    "dispute_categories": [
        ("list", "Dispute Categories"),
        ("detail", "Category Details"),
        ("eligibility", "Eligibility Screening"),
    ],
    "organizations": [
        ("list", "Organizations"),
        ("create", "Create Organization"),
        ("detail", "Organization"),
        ("edit", "Edit Organization"),
        ("members", "Organization Members"),
        ("invite", "Invite Member"),
        ("verify", "Verify Organization"),
        ("subscription", "Organization Subscription"),
    ],
    "verification": [
        ("dashboard", "Verification Dashboard"),
        ("submit", "Submit Verification"),
        ("kyc", "KYC Verification"),
        ("otp_send", "Send OTP"),
        ("otp_verify", "Verify OTP"),
        ("admin_list", "Verifications to Review"),
        ("review", "Review Verification"),
    ],
    "case_management": [
        ("dashboard", "Case Management Dashboard"),
        ("transfer", "Case Transfer"),
        ("withdrawal_request", "Withdrawal Request"),
        ("reopening_request", "Reopening Request"),
        ("notes", "Case Notes"),
        ("reminders", "Case Reminders"),
        ("withdrawal_requests", "Withdrawal Requests"),
        ("reopening_requests", "Reopening Requests"),
    ],
    "negotiation": [
        ("dashboard", "Negotiation Workspace"),
        ("room", "Negotiation Room"),
        ("proposal_create", "Create Settlement Proposal"),
        ("proposal_detail", "Proposal Details"),
        ("proposal_accept", "Accept Proposal"),
        ("proposal_reject", "Reject Proposal"),
        ("proposal_counter", "Counter Proposal"),
        ("proposal_withdraw", "Withdraw Proposal"),
        ("history", "Negotiation History"),
    ],
    "messaging": [
        ("threads", "Message Threads"),
        ("dispute_threads", "Dispute Discussions"),
        ("thread_create", "New Thread"),
        ("thread_detail", "Thread"),
        ("send", "Send Message"),
        ("mark_read", "Mark Read"),
        ("notifications", "Notifications"),
        ("notification_read", "Notification Read"),
        ("preferences", "Notification Preferences"),
    ],
    "documents": [
        ("list", "Documents"),
        ("dispute_documents", "Case Documents"),
        ("upload", "Upload Document"),
        ("detail", "Document Details"),
        ("download", "Download"),
        ("preview", "Preview Document"),
        ("replace", "Replace Document"),
        ("share", "Share Document"),
        ("delete", "Delete Document"),
        ("versions", "Document Versions"),
        ("folders", "Document Folders"),
        ("folder_create", "Create Folder"),
    ],
    "mediators": [
        ("directory", "Mediator Directory"),
        ("register", "Register as Mediator"),
        ("my_profile", "My Mediator Profile"),
        ("profile_edit", "Edit Mediator Profile"),
        ("availability", "My Availability Calendar"),
        ("public_profile", "Mediator Public Profile"),
        ("admin_list", "Mediator Verification Queue"),
        ("approve", "Approve Mediator"),
        ("suspend", "Suspend Mediator"),
        ("feedback_submit", "Submit Feedback"),
    ],
    "mediator_assignment": [
        ("dashboard", "Mediator Assignment Dashboard"),
        ("request", "Request Mediator Assignment"),
        ("accept", "Accept Assignment"),
        ("reject", "Reject Assignment"),
        ("replacement", "Request Mediator Replacement"),
        ("confirm", "Confirm Assignment"),
        ("coi", "Conflict of Interest Declaration"),
    ],
    "scheduling": [
        ("dashboard", "Scheduling Dashboard"),
        ("schedule", "Schedule Session"),
        ("session_detail", "Session Details"),
        ("reschedule", "Reschedule Session"),
        ("cancel", "Cancel Session"),
        ("complete", "Complete Session"),
        ("participants", "Session Participants"),
        ("my_calendar", "My Calendar"),
    ],
    "mediation_sessions": [
        ("room", "Online Mediation Room"),
        ("join", "Join Mediation Room"),
        ("participants", "Participants"),
        ("notes", "Session Notes"),
        ("caucus", "Private Caucus"),
        ("recording_consent", "Recording Consent"),
        ("close", "Close Room"),
    ],
    "settlements": [
        ("create", "Create Settlement"),
        ("detail", "Settlement Details"),
        ("sign", "Sign Settlement"),
        ("generate_doc", "Generate Settlement Document"),
        ("compliance", "Compliance Tracking"),
        ("mark_compliance_met", "Mark Compliance Met"),
    ],
    "digital_signatures": [
        ("request", "Request Signature"),
        ("sign", "Sign Document"),
        ("verify", "Verify Signature"),
        ("history", "Signature History"),
    ],
    "payments": [
        ("dashboard", "Payments Dashboard"),
        ("initiate", "Initiate Payment"),
        ("status", "Payment Status"),
        ("refund", "Request Refund"),
        ("refunds_admin", "Refunds Administration"),
        ("history", "Transaction History"),
        ("subscriptions", "Subscriptions"),
        ("invoices", "Tax Invoices"),
    ],
    "subscriptions": [
        ("dashboard", "Subscription Dashboard"),
        ("plans", "Subscription Plans"),
        ("subscribe", "Subscribe"),
        ("api_keys", "API Keys"),
        ("api_key_create", "Create API Key"),
        ("bulk_import", "Bulk Dispute Import"),
    ],
    "notifications": [
        ("dashboard", "Notifications Center"),
        ("mark_read", "Mark Notification Read"),
        ("unread_count", "Unread Count"),
        ("mark_all_read", "Mark All Read"),
        ("preferences", "Notification Preferences"),
    ],
    "grievances": [
        ("dashboard", "Grievances Dashboard"),
        ("file", "File a Complaint"),
        ("detail", "Complaint Details"),
        ("respond", "Respond to Complaint"),
        ("investigate", "Investigate Complaint"),
        ("appeal", "Appeal a Complaint"),
        ("assign", "Assign Complaint"),
        ("resolve", "Resolve Complaint"),
        ("feedback", "Submit Feedback"),
    ],
    "legal_compliance": [
        ("dashboard", "Compliance Dashboard"),
        ("consents", "Consent Records"),
        ("data_requests", "Data Subject Requests"),
        ("data_request_create", "Create Data Subject Request"),
        ("retention", "Data Retention Policies"),
        ("incidents", "Security Incidents"),
        ("coi", "Conflict of Interest Declarations"),
    ],
    "analytics": [
        ("dashboard", "ODR Analytics Dashboard"),
        ("snapshot", "Platform Snapshot"),
        ("categories", "Category Analytics"),
        ("mediators", "Mediator Performance"),
        ("generate", "Generate Snapshot"),
    ],
    "ai_assistant": [
        ("dashboard", "AI Assistant"),
        ("dispute_summary", "AI Dispute Summary"),
        ("settlement_draft", "AI Settlement Draft"),
        ("translation", "Translation Assistant"),
        ("history", "AI Session History"),
        ("review", "AI Session Review"),
    ],
    "core_dashboards": [
        ("home", "ResolveNow Dashboard"),
        ("individual", "Individual Dashboard"),
        ("my_claims", "My Claims"),
        ("my_responses", "My Responses"),
    ],
    "admin_dashboards": [
        ("home", "Admin Dashboard"),
        ("users", "User Management"),
        ("cases", "Case Monitoring"),
        ("categories", "Category Management"),
        ("fees", "Fee Configuration"),
        ("payments", "Payment Monitoring"),
        ("complaints", "Complaint Management"),
        ("content", "Content Management"),
        ("settings", "Platform Settings"),
        ("audit_logs", "Audit Logs"),
        ("security", "Security Monitoring"),
        ("reports", "System Reports"),
    ],
    "mediator_portals": [
        ("home", "Mediator Portal"),
        ("cases", "My Cases"),
        ("schedule", "My Schedule"),
        ("earnings", "My Earnings"),
        ("feedback", "My Feedback"),
    ],
    "legal_portals": [
        ("home", "Legal Professional Portal"),
        ("clients", "Client Management"),
        ("cases", "Legal Cases"),
        ("documents", "Legal Documents"),
        ("authorizations", "Client Authorizations"),
    ],
    "business_portals": [
        ("home", "Business Portal"),
        ("organizations", "Organizations"),
        ("cases", "Business Cases"),
        ("reports", "Corporate Reports"),
        ("billing", "Billing"),
        ("bulk_import", "Bulk Dispute Import"),
    ],
}


TEMPLATE_BODY = """{% extends "base.html" %}
{% block title %}{title} - ResolveNow{% endblock %}
{% block content %}
<div class="container py-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <div>
            <a href="{{% url 'dashboard:home' %}}" class="text-decoration-none small"><i class="bi bi-arrow-left"></i> Dashboard</a>
            <h2 class="fw-bold text-primary mb-0 mt-1">{icon} {title}</h2>
            <p class="text-muted mb-0">{description}</p>
        </div>
    </div>
    <div class="rn-card">
        <h5 class="rn-card-title">{title}</h5>
        <p class="text-muted">{description}</p>
        <p>This module is part of the ResolveNow ODR platform. Use the navigation at the top to explore the full platform.</p>
        <div class="row g-3 mt-2">
            <div class="col-md-6"><div class="border rounded p-3"><h6 class="text-primary">Module Information</h6><ul class="small mb-0"><li>App: <code>{app}</code></li><li>View: <code>{view}</code></li><li>Template: <code>{template_name}</code></li></ul></div></div>
            <div class="col-md-6"><div class="border rounded p-3"><h6 class="text-primary">Related Links</h6><ul class="small mb-0">{related_links}</ul></div></div>
        </div>
    </div>
</div>
{{% endblock %}}
"""

ICON_MAP = {
    "list": "bi-list-ul",
    "create": "bi-plus-circle",
    "detail": "bi-info-circle",
    "edit": "bi-pencil",
    "delete": "bi-trash",
    "dashboard": "bi-speedometer2",
    "default": "bi-bounding-box",
}

REL_LINKS = {
    "dispute_categories": [("categories:list", "All Categories"), ("disputes:create", "File Dispute"), ("disputes:list", "My Cases"), ("mediators:directory", "Mediators")],
    "organizations": [("organizations:list", "Organizations"), ("subscriptions:dashboard", "Subscriptions"), ("business_portal:home", "Business Portal"), ("disputes:create", "File Dispute")],
    "verification": [("verification:dashboard", "Verification"), ("accounts:profile", "My Profile"), ("legal_compliance:dashboard", "Compliance"), ("accounts:login_history", "Login History")],
    "case_management": [("case_management:dashboard", "Case Management"), ("disputes:list", "All Cases"), ("analytics:dashboard", "Analytics"), ("audit_logs", "Audit Logs")],
    "negotiation": [("negotiation:dashboard", "Negotiation"), ("disputes:list", "My Cases"), ("messaging:threads", "Messages"), ("settlements:create", "Settlements")],
    "messaging": [("messaging:threads", "Messages"), ("notifications:dashboard", "Notifications"), ("disputes:list", "Cases"), ("messaging:preferences", "Preferences")],
    "documents": [("documents:list", "Documents"), ("disputes:list", "Cases"), ("documents:folders", "Folders"), ("documents:upload", "Upload")],
    "mediators": [("mediators:directory", "Mediators"), ("mediator_portal:home", "Mediator Portal"), ("mediator_assignment:dashboard", "Assignments"), ("analytics:mediators", "Performance")],
    "mediator_assignment": [("mediator_assignment:dashboard", "Assignments"), ("mediators:directory", "Mediators"), ("disputes:list", "Cases"), ("mediators:my_profile", "My Profile")],
    "scheduling": [("scheduling:dashboard", "Scheduling"), ("scheduling:my_calendar", "My Calendar"), ("mediation_sessions:room", "Mediation Room"), ("disputes:list", "Cases")],
    "mediation_sessions": [("mediation_sessions:room", "Mediation Room"), ("scheduling:dashboard", "Scheduling"), ("disputes:list", "Cases"), ("messaging:threads", "Messages")],
    "settlements": [("settlements:create", "Settlements"), ("negotiation:dashboard", "Negotiation"), ("disputes:list", "Cases"), ("digital_signatures:history", "Signatures")],
    "digital_signatures": [("digital_signatures:history", "Signatures"), ("documents:list", "Documents"), ("settlements:detail", "Settlements"), ("audit_logs", "Audit Logs")],
    "payments": [("payments:dashboard", "Payments"), ("payments:invoices", "Invoices"), ("subscriptions:plans", "Plans"), ("payments:history", "History")],
    "subscriptions": [("subscriptions:dashboard", "Subscriptions"), ("subscriptions:plans", "Plans"), ("payments:dashboard", "Payments"), ("business_portal:billing", "Billing")],
    "notifications": [("notifications:dashboard", "Notifications"), ("messaging:threads", "Messages"), ("accounts:profile", "Profile"), ("notifications:preferences", "Preferences")],
    "grievances": [("grievances:dashboard", "Grievances"), ("grievances:file", "File Complaint"), ("grievances:feedback", "Feedback"), ("admin_dash:complaints", "Admin Complaints")],
    "legal_compliance": [("legal_compliance:dashboard", "Compliance"), ("legal_compliance:consents", "Consents"), ("legal_compliance:retention", "Retention"), ("legal_compliance:incidents", "Incidents")],
    "analytics": [("analytics:dashboard", "Analytics"), ("analytics:categories", "Categories"), ("analytics:mediators", "Mediators"), ("admin_dash:reports", "Reports")],
    "ai_assistant": [("ai_assistant:dashboard", "AI Assistant"), ("ai_assistant:dispute_summary", "Dispute Summary"), ("ai_assistant:settlement_draft", "Settlement Draft"), ("ai_assistant:translation", "Translation")],
    "core_dashboards": [("dashboard:home", "Dashboard"), ("disputes:list", "Cases"), ("documents:list", "Documents"), ("messaging:threads", "Messages")],
    "admin_dashboards": [("admin_dash:home", "Admin"), ("admin_dash:users", "Users"), ("admin_dash:cases", "Cases"), ("admin_dash:audit_logs", "Audit Logs")],
    "mediator_portals": [("mediator_portal:home", "Mediator Portal"), ("mediators:my_profile", "Profile"), ("mediator_portal:cases", "Cases"), ("mediator_portal:earnings", "Earnings")],
    "legal_portals": [("legal_portal:home", "Legal Portal"), ("legal_portal:clients", "Clients"), ("legal_portal:cases", "Cases"), ("legal_portal:documents", "Documents")],
    "business_portals": [("business_portal:home", "Business Portal"), ("business_portal:organizations", "Organizations"), ("business_portal:cases", "Cases"), ("business_portal:billing", "Billing")],
}


DESCRIPTIONS = {
    "list": "Browse and manage records in this module.",
    "create": "Create a new record.",
    "detail": "View details of the selected record.",
    "edit": "Edit the selected record.",
    "dashboard": "Main dashboard for this module.",
    "delete": "Permanently remove the record.",
}


def generate_template(app, slug, title):
    icon = ICON_MAP.get(slug, ICON_MAP["default"])
    desc = DESCRIPTIONS.get(slug, "ResolveNow ODR platform module.")
    related = ""
    for url_name, label in REL_LINKS.get(app, []):
        related += f'<li><a href="{{% url \'{url_name}\' %}}">{label}</a></li>\n'
    body = (
        '{% extends "base.html" %}\n'
        "{% block title %}" + title + " - ResolveNow{% endblock %}\n"
        "{% block content %}\n"
        '<div class="container py-4">\n'
        '    <div class="d-flex justify-content-between align-items-center mb-4">\n'
        '        <div>\n'
        '            <a href="{% url \'dashboard:home\' %}" class="text-decoration-none small"><i class="bi bi-arrow-left"></i> Dashboard</a>\n'
        '            <h2 class="fw-bold text-primary mb-0 mt-1"><i class="bi ' + icon + ' me-2"></i>' + title + '</h2>\n'
        '            <p class="text-muted mb-0">' + desc + '</p>\n'
        '        </div>\n'
        '    </div>\n'
        '    <div class="rn-card">\n'
        '        <h5 class="rn-card-title">' + title + '</h5>\n'
        '        <p class="text-muted">' + desc + ' This is part of the ResolveNow Online Dispute Resolution (ODR) platform covering 24 Django apps and 22 feature areas.</p>\n'
        '        <div class="row g-3 mt-2">\n'
        '            <div class="col-md-6"><div class="border rounded p-3"><h6 class="text-primary">Module</h6><ul class="small mb-0"><li>App: <code>' + app + '</code></li><li>View: <code>' + slug + '</code></li></ul></div></div>\n'
        '            <div class="col-md-6"><div class="border rounded p-3"><h6 class="text-primary">Related Links</h6><ul class="small mb-0">' + related + '</ul></div></div>\n'
        '        </div>\n'
        '    </div>\n'
        '</div>\n'
        "{% endblock %}\n"
    )
    return body


count = 0
for app, specs in TEMPLATE_SPECS.items():
    template_dir = os.path.join(BASE, "templates", app)
    os.makedirs(template_dir, exist_ok=True)
    for slug, title in specs:
        path = os.path.join(template_dir, f"{slug}.html")
        with open(path, "w") as f:
            f.write(generate_template(app, slug, title))
        count += 1
print(f"Generated {count} templates")
