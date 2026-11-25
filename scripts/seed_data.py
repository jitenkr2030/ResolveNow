"""Seed demo data for ResolveNow ODR Platform.

Run: python manage.py shell < scripts/seed_data.py
or:  python manage.py load_seed
"""
import os
import sys
import random
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "resolvenow_config.settings")
django.setup()

from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import uuid

User = get_user_model()

# ------------------ 1. Super Admin ------------------
print("Creating super admin...")
admin_user, created = User.objects.get_or_create(
    email="admin@resolvenow.in",
    defaults={
        "first_name": "Platform",
        "last_name": "Administrator",
        "role": "super_admin",
        "is_staff": True,
        "is_superuser": True,
        "is_email_verified": True,
        "is_mobile_verified": True,
        "identity_verified": True,
        "is_active": True,
        "consent_terms_of_service": True,
        "consent_privacy_policy": True,
        "consent_timestamp": timezone.now(),
    },
)
if created:
    admin_user.set_password("ResolveNow2026!")
    admin_user.save()
    print(f"  Created super admin: admin@resolvenow.in")
else:
    print(f"  Super admin already exists")


# ------------------ 2. Demo users ------------------
print("Creating demo users...")
demo_users = [
    {
        "email": "priya.sharma@example.com",
        "first_name": "Priya",
        "last_name": "Sharma",
        "role": "individual",
        "phone_number": "+91-9810012345",
        "city": "Mumbai",
        "state": "Maharashtra",
    },
    {
        "email": "rajesh.kumar@example.com",
        "first_name": "Rajesh",
        "last_name": "Kumar",
        "role": "respondent",
        "phone_number": "+91-9811122334",
        "city": "Delhi",
        "state": "Delhi",
    },
    {
        "email": "advocate.singh@legalfirm.in",
        "first_name": "Adv.",
        "last_name": "Singh",
        "role": "lawyer",
        "phone_number": "+91-9812233445",
        "city": "Bangalore",
        "state": "Karnataka",
    },
    {
        "email": "mediator.nair@mediation.in",
        "first_name": "Adv.",
        "last_name": "Nair",
        "role": "mediator",
        "phone_number": "+91-9823344556",
        "city": "Kochi",
        "state": "Kerala",
    },
    {
        "email": "corporate@techstartup.in",
        "first_name": "Tech",
        "last_name": "Startup",
        "role": "business",
        "phone_number": "+91-9834455667",
        "city": "Pune",
        "state": "Maharashtra",
    },
    {
        "email": "case.manager@resolvenow.in",
        "first_name": "Case",
        "last_name": "Manager",
        "role": "case_manager",
        "is_staff": True,
        "phone_number": "+91-9845566778",
        "city": "Hyderabad",
        "state": "Telangana",
    },
    {
        "email": "finance@resolvenow.in",
        "first_name": "Finance",
        "last_name": "Manager",
        "role": "finance_manager",
        "is_staff": True,
        "phone_number": "+91-9856677889",
        "city": "Chennai",
        "state": "Tamil Nadu",
    },
    {
        "email": "grievance@resolvenow.in",
        "first_name": "Grievance",
        "last_name": "Officer",
        "role": "grievance_officer",
        "is_staff": True,
        "phone_number": "+91-9867788990",
        "city": "Mumbai",
        "state": "Maharashtra",
    },
    {
        "email": "platform.admin@resolvenow.in",
        "first_name": "Platform",
        "last_name": "Admin",
        "role": "administrator",
        "is_staff": True,
        "phone_number": "+91-9878899001",
        "city": "Mumbai",
        "state": "Maharashtra",
    },
]

for u in demo_users:
    password = u.pop("password", "ResolveNow2026!")
    user, created = User.objects.get_or_create(
        email=u["email"],
        defaults={
            **u,
            "is_email_verified": True,
            "is_mobile_verified": True,
            "identity_verified": True,
            "is_active": True,
            "consent_terms_of_service": True,
            "consent_privacy_policy": True,
            "consent_timestamp": timezone.now(),
        },
    )
    if created:
        user.set_password(password)
        user.save()
        print(f"  Created user: {user.email} ({user.get_role_display()})")


# ------------------ 3. Dispute Categories ------------------
print("Creating dispute categories...")
from dispute_categories.models import DisputeCategory, LegalEligibilityChecklist

category_data = [
    ("Commercial", "commercial", "Business and contractual disputes"),
    ("Financial", "financial", "Outstanding payments and invoices"),
    ("Employment", "employment", "Workplace and employment disputes"),
    ("Consumer", "consumer", "Product and service complaints"),
    ("Property", "property", "Rental and property-related disputes"),
    ("Partnership", "partnership", "Business partnership disagreements"),
    ("Family", "family", "Suitable family and personal disputes"),
    ("Housing", "housing", "Resident and housing society disputes"),
    ("Education", "education", "Institutional fee and service disputes"),
    ("Vendor", "vendor", "Supplier and customer disagreements"),
    ("Technology", "technology", "IT service and software contracts"),
    ("Insurance", "insurance", "Suitable insurance-related disputes"),
]

for idx, (name, slug, desc) in enumerate(category_data):
    cat, created = DisputeCategory.objects.get_or_create(
        slug=slug,
        defaults={
            "name": name,
            "description": f"{name} category - {desc.lower()}.",
            "examples": desc,
            "display_order": idx,
            "is_active": True,
        },
    )
    if created:
        print(f"  Created category: {name}")

# Add eligibility questions for one category as a sample
if not LegalEligibilityChecklist.objects.exists():
    commercial = DisputeCategory.objects.get(slug="commercial")
    questions = [
        ("Is this dispute related to a criminal offense?", True, True),
        ("Are both parties willing to participate in mediation voluntarily?", True, False),
        ("Is the disputed amount above the category minimum?", False, False),
        ("Have the parties attempted any direct communication about the dispute?", True, False),
        ("Are there any pending court cases related to this dispute?", True, True),
    ]
    for idx, (q, required, disq) in enumerate(questions):
        LegalEligibilityChecklist.objects.create(
            category=commercial,
            question=q,
            is_required=required,
            disqualifying_if_yes=disq,
            display_order=idx,
        )
    print("  Created 5 eligibility questions for Commercial category")


# ------------------ 4. Mediator Profile ------------------
print("Creating mediator profile...")
from mediators.models import MediatorProfile
mediator_user = User.objects.get(email="mediator.nair@mediation.in")
mp, created = MediatorProfile.objects.get_or_create(
    user=mediator_user,
    defaults={
        "professional_title": "Senior Mediator & Advocate",
        "bio": "Experienced mediator with 12+ years specializing in commercial, financial and employment disputes. Member of the Indian Institute of Arbitration & Mediation.",
        "years_of_experience": 12,
        "qualifications": ["LL.M, NLSIU Bangalore", "Certified Mediator - IIAM"],
        "certifications": ["IIAM Certified Mediator", "ICAI Arbitrator"],
        "practice_areas": ["commercial", "financial", "employment"],
        "specializations": ["Commercial Contracts", "Employment Disputes", "Partnership Disputes"],
        "languages_spoken": ["English", "Malayalam", "Hindi", "Tamil"],
        "geographic_coverage": ["Kerala", "Tamil Nadu", "Karnataka", "Pan-India (online)"],
        "bar_council_registration": "KL/1234/2010",
        "mediator_registration_number": "IIAM-MED-2021-0123",
        "hourly_fee": 3000,
        "half_day_fee": 18000,
        "full_day_fee": 30000,
        "approval_status": "approved",
        "rating": 4.7,
        "total_ratings": 28,
        "total_cases_handled": 142,
        "successful_settlements": 124,
        "success_rate": 87.32,
        "is_accepting_new_cases": True,
        "approved_at": timezone.now() - timedelta(days=180),
    },
)
if created:
    print(f"  Created mediator profile for {mediator_user.email}")


# ------------------ 5. Sample Dispute ------------------
print("Creating sample dispute...")
from disputes.models import Dispute, DisputeParty, DisputeTimelineEntry
claimant = User.objects.get(email="priya.sharma@example.com")
respondent = User.objects.get(email="rajesh.kumar@example.com")
commercial_cat = DisputeCategory.objects.get(slug="commercial")
case_manager = User.objects.get(email="case.manager@resolvenow.in")

dispute, created = Dispute.objects.get_or_create(
    case_ref__startswith="RN-",
    defaults={
        "case_ref": "RN-2026-DEMO01",
        "title": "Unpaid Software Development Fees - Tech Contract Dispute",
        "description": "The claimant (freelance software developer) was engaged by the respondent (small business) to build a custom e-commerce platform for an agreed sum of Rs 4,50,000. The respondent paid an initial deposit of Rs 1,00,000 but has not paid the remaining Rs 3,50,000 despite the platform being delivered and accepted on 15 Feb 2026. Multiple email and WhatsApp communications have not resulted in payment.",
        "category": commercial_cat,
        "sub_category": "IT Service Contract",
        "claimant": claimant,
        "disputed_amount": 350000,
        "currency": "INR",
        "is_amount_confidential": False,
        "agreement_reference": "ECOMM-DEV-2025-11",
        "agreement_date": timezone.now() - timedelta(days=120),
        "agreement_summary": "Software development contract for e-commerce platform. Rs 1L advance, Rs 3.5L on delivery.",
        "previous_communication_history": "Emails dated 16-Feb, 22-Feb, 03-Mar, 18-Mar, 02-Apr 2026. WhatsApp messages dated 09-Apr, 15-Apr 2026.",
        "requested_resolution": "Payment of the outstanding Rs 3,50,000 within 30 days of mediation, with interest at 12% per annum until paid in full.",
        "jurisdiction": "India",
        "location_of_dispute": "Mumbai, Maharashtra",
        "status": "submitted",
        "priority": "high",
        "is_confidential": True,
        "assigned_case_manager": case_manager,
        "submitted_at": timezone.now() - timedelta(days=5),
        "acknowledged_at": timezone.now() - timedelta(days=4),
        "response_deadline": timezone.now() + timedelta(days=10),
        "negotiation_deadline": timezone.now() + timedelta(days=25),
    },
)

if created:
    print(f"  Created dispute: {dispute.case_ref}")
    # Add parties
    DisputeParty.objects.create(
        dispute=dispute,
        user=claimant,
        role="claimant",
        invitation_status="accepted",
        joined_at=timezone.now() - timedelta(days=5),
        contact_email=claimant.email,
        has_accepted_jurisdiction=True,
        has_signed_confidentiality=True,
    )
    DisputeParty.objects.create(
        dispute=dispute,
        user=respondent,
        role="respondent",
        invitation_status="pending",
        contact_email=respondent.email,
        contact_phone=respondent.phone_number,
    )

    # Timeline
    DisputeTimelineEntry.objects.create(
        dispute=dispute,
        entry_type="created",
        title="Dispute case created",
        description=f"Draft dispute created by {claimant.email}",
        actor=claimant,
        created_at=timezone.now() - timedelta(days=5),
    )
    DisputeTimelineEntry.objects.create(
        dispute=dispute,
        entry_type="submitted",
        title="Dispute application submitted",
        description=f"Submitted and acknowledged on {timezone.now() - timedelta(days=4):%Y-%m-%d}",
        actor=claimant,
        created_at=timezone.now() - timedelta(days=4),
    )
    DisputeTimelineEntry.objects.create(
        dispute=dispute,
        entry_type="party_invited",
        title=f"Party invitation sent to {respondent.email}",
        description="Invited as respondent",
        actor=claimant,
        created_at=timezone.now() - timedelta(days=3),
    )
    DisputeTimelineEntry.objects.create(
        dispute=dispute,
        entry_type="status_change",
        title="Case assigned to Case Manager",
        description=f"Assigned to {case_manager.email}",
        actor=admin_user,
        created_at=timezone.now() - timedelta(days=2),
    )


# ------------------ 6. Payment ------------------
print("Creating payment record...")
from payments.models import Payment
pay, created = Payment.objects.get_or_create(
    payment_ref__startswith="PAY-DEMO",
    defaults={
        "payment_ref": "PAY-DEMO-0001",
        "user": claimant,
        "dispute": dispute,
        "payment_type": "registration_fee",
        "amount": 1500,
        "tax_amount": 270,
        "total_amount": 1770,
        "status": "successful",
        "payment_gateway": "razorpay",
        "gateway_transaction_id": "rzp_demo_001",
        "invoice_number": "INV-2026-0001",
        "paid_at": timezone.now() - timedelta(days=5),
    },
)
if created:
    print(f"  Created payment: {pay.payment_ref}")


# ------------------ 7. Sample Complaint ------------------
print("Creating sample complaint...")
from grievances.models import Complaint
complaint, created = Complaint.objects.get_or_create(
    complaint_ref="GRV-DEMO-0001",
    defaults={
        "complainant": claimant,
        "complaint_type": "platform",
        "priority": "medium",
        "subject": "Difficulty uploading large PDF documents",
        "description": "When uploading PDFs larger than 20MB, the upload occasionally fails. Smaller files upload fine.",
        "status": "submitted",
        "submitted_at": timezone.now() - timedelta(days=1),
    },
)
if created:
    print(f"  Created complaint: {complaint.complaint_ref}")


# ------------------ 8. Eligibility Result ------------------
print("Creating eligibility result for sample dispute...")
from dispute_categories.models import DisputeEligibilityResult
elig, created = DisputeEligibilityResult.objects.get_or_create(
    dispute=dispute,
    defaults={
        "reviewed_by": case_manager,
        "is_eligible": True,
        "eligibility_score": 100,
        "notes": "Commercial dispute of unpaid fees - eligible for ODR.",
        "decision": "eligible",
        "reviewed_at": timezone.now() - timedelta(days=1),
        "requires_human_review": False,
    },
)
if created:
    print(f"  Created eligibility result: {elig.decision}")


# ------------------ 9. Security Incident ------------------
print("Creating security incident record...")
from legal_compliance.models import SecurityIncident, ConsentRecord
inc, created = SecurityIncident.objects.get_or_create(
    title="Sample - failed login attempts detected",
    defaults={
        "description": "20 failed login attempts from a single IP detected. Account lockout triggered. No data compromised.",
        "severity": "low",
        "status": "resolved",
        "resolution_summary": "Account lockout held, password reset by user.",
        "detected_at": timezone.now() - timedelta(days=7),
        "resolved_at": timezone.now() - timedelta(days=6),
    },
)
if created:
    print(f"  Created security incident")

# Consent records for the claimant
for ctype in ["terms_of_service", "privacy_policy", "data_processing"]:
    ConsentRecord.objects.get_or_create(
        user=claimant,
        consent_type=ctype,
        defaults={
            "consent_version": "1.0",
            "is_given": True,
            "given_at": timezone.now() - timedelta(days=10),
            "is_active": True,
        },
    )


# ------------------ 10. Notification ------------------
print("Creating notifications...")
from messaging.models import Notification
Notification.objects.create(
    recipient=claimant,
    notification_type="case_registration",
    channel="in_platform",
    subject=f"Case {dispute.case_ref} submitted successfully",
    body=f"Your dispute '{dispute.title}' has been submitted and acknowledged. Case manager will be assigned soon.",
    dispute=dispute,
    related_url=f"/disputes/{dispute.pk}/",
)
Notification.objects.create(
    recipient=respondent,
    notification_type="party_invitation",
    channel="in_platform",
    subject=f"You have been invited to respond to case {dispute.case_ref}",
    body=f"{claimant.get_full_name()} has filed a dispute and named you as respondent. Please log in to review and respond.",
    dispute=dispute,
    related_url=f"/disputes/{dispute.pk}/",
)
Notification.objects.create(
    recipient=case_manager,
    notification_type="case_status_update",
    channel="in_platform",
    subject=f"New case {dispute.case_ref} assigned to you",
    body="A new case has been assigned to your management queue.",
    dispute=dispute,
    related_url=f"/disputes/{dispute.pk}/",
)
print(f"  Created notifications")


print("\n" + "="*60)
print("Seed data created successfully!")
print("="*60)
print("\nLogin credentials:")
print(f"  Super Admin:    admin@resolvenow.in / ResolveNow2026!")
print(f"  Individual user: priya.sharma@example.com / ResolveNow2026!")
print(f"  Respondent:     rajesh.kumar@example.com / ResolveNow2026!")
print(f"  Lawyer:          advocate.singh@legalfirm.in / ResolveNow2026!")
print(f"  Mediator:        mediator.nair@mediation.in / ResolveNow2026!")
print(f"  Business:        corporate@techstartup.in / ResolveNow2026!")
print(f"  Case Manager:    case.manager@resolvenow.in / ResolveNow2026!")
print(f"  Finance:         finance@resolvenow.in / ResolveNow2026!")
print(f"  Grievance:       grievance@resolvenow.in / ResolveNow2026!")
print(f"  Admin:           platform.admin@resolvenow.in / ResolveNow2026!")
