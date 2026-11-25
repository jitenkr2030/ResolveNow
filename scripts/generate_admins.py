#!/usr/bin/env python3
"""Generate admin.py registrations for all ResolveNow apps."""
import os

BASE = "/home/z/my-project"

# App -> list of model classes
APP_MODELS = {
    "accounts": ["User", "LoginHistory", "AccountDeletionRequest"],
    "user_profiles": ["UserProfile", "OrganizationMembership"],
    "organizations": ["Organization", "Subscription"],
    "verification": ["VerificationRecord", "OTPVerification"],
    "dispute_categories": ["DisputeCategory", "LegalEligibilityChecklist", "DisputeEligibilityResult"],
    "disputes": ["Dispute", "DisputeParty", "DisputeTimelineEntry"],
    "case_management": ["CaseTransfer", "CaseWithdrawalRequest", "CaseReopeningRequest", "CaseReminder", "CaseNote", "CaseArchive"],
    "negotiation": ["NegotiationRoom", "SettlementProposal", "ProposalResponse", "NegotiationActivity"],
    "messaging": ["MessageThread", "Message", "Notification", "NotificationPreference"],
    "documents": ["Document", "DocumentFolder", "DocumentAccessLog"],
    "mediators": ["MediatorProfile", "MediatorAvailability", "MediatorFeedback", "ConflictOfInterestDeclaration"],
    "mediator_assignment": ["MediatorAssignmentRequest", "MediatorReplacementRequest", "AssignmentHistory"],
    "scheduling": ["ScheduledSession", "SessionParticipant", "RescheduleRequest"],
    "mediation_sessions": ["MediationRoom", "RoomParticipant", "SessionNote", "PrivateCaucus"],
    "settlements": ["SettlementRecord", "SettlementSignature", "SettlementComplianceRecord"],
    "digital_signatures": ["DigitalSignature"],
    "payments": ["Payment", "RefundRequest", "TaxInvoice", "SubscriptionPlan"],
    "subscriptions": ["Subscription", "APIKey", "BulkDisputeImport"],
    "grievances": ["Complaint", "ComplaintResponse", "ComplaintAppeal", "Feedback", "GrievanceInvestigation"],
    "legal_compliance": ["ConsentRecord", "DataSubjectRequest", "DataRetentionPolicy", "SecurityIncident", "ConflictOfInterestDeclaration"],
    "audit_logs": ["AuditLog", "SystemConfigurationLog"],
    "analytics": ["AnalyticsSnapshot", "CategoryAnalytics", "MediatorPerformanceMetric"],
    "ai_assistant": ["AIAssistantSession", "AISettlementDraft", "TranslationJob"],
}


for app, models in APP_MODELS.items():
    admin_path = os.path.join(BASE, app, "admin.py")
    lines = [
        f'from django.contrib import admin',
        f'from .models import {", ".join(models)}',
        "",
    ]
    for m in models:
        lines.append(f"@admin.register({m})")
        lines.append(f"class {m}Admin(admin.ModelAdmin):")
        lines.append(f'    list_display = ("id", "__str__")')
        lines.append(f'    search_fields = ()')
        lines.append("")
    with open(admin_path, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"  created {admin_path}")

print("Done.")
