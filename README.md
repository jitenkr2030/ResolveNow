# ResolveNow - Online Dispute Resolution (ODR) Platform

**Resolve Disputes Online. Fairly. Efficiently.**

A comprehensive Django-based Online Dispute Resolution platform enabling individuals, businesses, lawyers and professional mediators to resolve suitable disputes through online negotiation, mediation, secure communication and documented settlements — without necessarily going through conventional litigation.

## Features

ResolveNow implements **24 Django apps** covering **22 feature areas** of a complete ODR workflow:

### 1. User Registration & Account Management
- Custom user model with role-based access (11 roles)
- Multi-role registration: Individual, Business, Lawyer, Mediator
- Email verification, mobile verification, KYC
- Profile management, login history, device tracking
- MFA, account suspension, deletion requests

### 2. Dispute Registration & Case Filing
- Create disputes in 12 categories
- Identify claimant/respondent, add multiple parties
- Upload supporting documents, agreements, communication history
- Specify disputed amount, requested resolution
- Save drafts, submit, generate unique case reference (RN-YYYY-XXXXXX)
- Track application status publicly

### 3. Dispute Categories Management
12 categories: Commercial, Financial, Employment, Consumer, Property, Partnership, Family, Housing, Education, Vendor, Technology, Insurance. Legal eligibility screening per category.

### 4. Case Management System
- Centralized case dashboard with status workflow (12 statuses)
- Case assignment, priority, transfer, withdrawal, closure
- Case timeline, activity history, admin notes, reminders
- Reopening requests, archive and retrieval

### 5. Online Negotiation Workspace
- Private negotiation rooms, secure messaging
- Initial offers, counteroffers, revised proposals
- Accept/reject, negotiation history, deadlines
- Payment proposal management, instalment schedules
- Mediator-assisted negotiation

### 6. Secure Document Management
- Upload PDF, DOCX, XLSX, images
- Categorization, private folders, access permissions
- Version history, replacement, expiry controls
- Access & download logs
- Evidence submission with authenticity declarations

### 7. Mediator Registration & Management
- Professional profile creation
- Qualification & experience verification
- Practice areas, languages, geographic coverage
- Availability calendar, fee configuration
- Approval workflow, performance records, feedback & ratings

### 8. Mediator Assignment System
- Browse, search by category/language/specialization
- Party-requested and mutual selection
- Mediator invitation, acceptance, rejection
- Conflict-of-interest declaration
- Replacement requests, assignment confirmation, history

### 9. Mediation Scheduling & Calendar
- Schedule sessions, manage availability
- Reschedule / cancellation requests
- Session reminders, calendar integration, time-zone management
- Multiple session scheduling, attendance records

### 10. Online Mediation Room
- Secure video/audio conferencing
- Private caucus rooms, separate party sessions
- Screen sharing, document presentation
- Waiting room, participant controls, attendance
- Session notes, mediator summaries
- **Recording disabled by default; only enabled where lawful with consent**

### 11. Settlement Proposal Management
- Create settlement proposals with terms
- Payment amount, deadlines, instalment schedules
- Obligations of each party, conditions
- Accept/reject/request modifications, history tracking
- Partial settlements supported

### 12. Settlement Record Management
- Generate settlement documents & summaries
- Capture signatures, timestamp records
- Document versions, downloadable copies
- Audit trails, completion status
- Compliance tracking with payment milestones
- **Distinguishes between informal settlement records and mediated settlement agreements that satisfy statutory requirements**

### 13. Payment & Billing Management
- Case registration fees, platform service charges, mediator fees
- Payment gateway integration (Razorpay/PayU/Stripe/UPI)
- Receipts, tax invoice generation, refund management
- Subscription management, transaction history

### 14. Communication & Notification System
- In-platform messaging, email, SMS, WhatsApp (with consent)
- Case registration, document submission, mediator assignment alerts
- Meeting reminders, settlement proposal, payment notifications
- Deadline reminders, case status updates, administrative announcements
- User notification preferences

### 15. Dispute Resolution Workflow Automation
- Automatic case reference generation
- Application completeness checks
- Eligibility screening, duplicate detection
- Party invitation automation
- Deadline tracking, scheduling workflow
- Settlement document generation, case closure workflow
- **Automation never makes legal eligibility or settlement decisions without human review**

### 16. Legal Professional Portal
- Professional registration, client case management
- Case document review, client communication
- Mediation participation, settlement proposal review
- Legal document upload, case progress monitoring
- Client authorization management

### 17. Business & Corporate Portal
- Organization registration, business verification
- Multiple employee accounts, role-based permissions
- Bulk dispute registration, vendor/customer/contract disputes
- Invoice dispute registration, outstanding payment tracking
- Multiple case dashboard, corporate reporting
- Subscription billing, API integrations

### 18. Admin & Super Admin Dashboard
- Total registered users, total disputes, pending applications
- Active mediation cases, unassigned cases
- Registered mediators, mediator verification
- User management, case monitoring
- Dispute category management, fee configuration
- Payment monitoring, refund approval
- Complaint management, content management
- Platform settings, audit log management, access control
- System reports, security monitoring

### 19. Feedback, Complaint & Grievance Management
- Platform & mediator complaints
- Report inappropriate conduct, service quality feedback
- Complaint tracking, grievance assignment & investigation
- Response deadlines, complaint resolution
- Appeal/review requests, feedback analytics

### 20. Security, Privacy & Compliance
- Role-based access control, MFA
- Encryption in transit and at rest
- Secure document access, data backup & recovery
- Activity audit trails, login monitoring, session management
- Consent management, confidentiality controls
- Privacy policy management, data retention policies
- Data deletion workflows, security incident management
- Conflict-of-interest declarations, mediator impartiality safeguards
- **Indian data-protection (DPDP) compliance**

### 21. Advanced Features (Future-ready)
- AI Dispute Assistant (summarize, organize, missing info, neutral case summaries)
- AI Settlement Drafting Assistant (draft terms for human review)
- Multilingual Mediation (Hindi, English, regional Indian languages)
- ODR Analytics (dispute categories, resolution timelines, mediator workload)
- Digital Agreement Execution (e-signing, identity authentication, timestamps)

### 22. User Roles and Permissions
| Role | Main functions |
|------|---------------|
| Individual | Register and manage disputes |
| Claimant | File and manage claims |
| Respondent | Respond and negotiate |
| Business | Manage organizational disputes |
| Lawyer | Assist authorized clients |
| Mediator | Conduct mediation |
| Case Manager | Coordinate cases |
| Finance Manager | Manage billing |
| Grievance Officer | Handle complaints |
| Administrator | Manage platform operations |
| Super Admin | Manage entire platform |

## Project Structure

```
resolvenow/                  <- project root
├── manage.py
├── resolvenow_config/       <- Django project config (settings, urls, wsgi)
├── accounts/                <- Users, registration, login
├── organizations/           <- Business / corporate accounts
├── user_profiles/          <- Extended user profiles
├── verification/            <- KYC / identity verification
├── disputes/               <- Dispute registration & case filing (CORE)
├── case_management/        <- Case workflow, transfer, withdrawal
├── dispute_categories/     <- 12 dispute categories, eligibility
├── negotiation/            <- Negotiation workspace, proposals
├── messaging/              <- Secure messaging, notifications
├── documents/              <- Secure document management
├── mediators/              <- Mediator profiles, feedback, availability
├── mediator_assignment/    <- Assignment workflow, COI declarations
├── scheduling/             <- Session scheduling, calendar
├── mediation_sessions/     <- Online mediation room, caucus
├── settlements/            <- Settlement records, signatures, compliance
├── digital_signatures/    <- E-signing, document integrity
├── payments/               <- Payments, billing, invoices, refunds
├── subscriptions/          <- Subscription plans, API keys, bulk imports
├── notifications/          <- Notification center, preferences
├── grievances/             <- Complaints, feedback, investigations
├── legal_compliance/       <- Consents, data subject requests, incidents
├── audit_logs/             <- Activity audit trail
├── analytics/              <- ODR analytics, snapshots
├── ai_assistant/           <- AI dispute assistant, settlement drafting
├── core_dashboards/        <- User dashboard routing
├── admin_dashboards/       <- Admin & super admin dashboard
├── mediator_portals/      <- Mediator portal
├── legal_portals/          <- Legal professional portal
├── business_portals/       <- Business & corporate portal
├── templates/              <- All HTML templates (Bootstrap 5)
├── static/css/             <- Custom styles
├── static/js/              <- Custom JavaScript
├── scripts/                <- Utility scripts (seed, generate)
└── db.sqlite3              <- SQLite database
```

## Getting Started

### Installation

```bash
# Install dependencies
pip install django django-crispy-forms crispy-bootstrap4 user-agents pillow reportlab weasyprint

# Apply migrations
python manage.py migrate

# Seed demo data
DJANGO_SETTINGS_MODULE=resolvenow_config.settings python manage.py shell < scripts/seed_data.py

# Collect static files
python manage.py collectstatic --noinput

# Run development server
python manage.py runserver
```

### Access the platform

Open http://127.0.0.1:8000/ in your browser.

### Demo Credentials

| Role | Email | Password |
|------|-------|----------|
| Super Admin | admin@resolvenow.in | ResolveNow2026! |
| Individual / Claimant | priya.sharma@example.com | ResolveNow2026! |
| Respondent | rajesh.kumar@example.com | ResolveNow2026! |
| Lawyer | advocate.singh@legalfirm.in | ResolveNow2026! |
| Mediator | mediator.nair@mediation.in | ResolveNow2026! |
| Business User | corporate@techstartup.in | ResolveNow2026! |
| Case Manager | case.manager@resolvenow.in | ResolveNow2026! |
| Finance Manager | finance@resolvenow.in | ResolveNow2026! |
| Grievance Officer | grievance@resolvenow.in | ResolveNow2026! |
| Administrator | platform.admin@resolvenow.in | ResolveNow2026! |

## Key URLs

| URL | Description |
|-----|-------------|
| `/` | Landing page |
| `/accounts/login/` | Sign in |
| `/accounts/register/` | Multi-role registration |
| `/accounts/profile/` | Profile management |
| `/accounts/login-history/` | Login & device history |
| `/dashboard/` | User dashboard (role-based) |
| `/disputes/` | List of disputes |
| `/disputes/create/` | File a new dispute |
| `/disputes/<pk>/` | Dispute detail (parties, documents, timeline, proposals, sessions, payments, messages, settlements) |
| `/disputes/track/` | Track application status by case ref |
| `/case-management/` | Case management dashboard |
| `/categories/` | All 12 dispute categories |
| `/negotiation/` | Negotiation workspace |
| `/messaging/` | Secure messaging |
| `/documents/` | Document management |
| `/mediators/` | Mediator directory |
| `/mediator-assignment/` | Mediator assignment |
| `/scheduling/` | Mediation scheduling |
| `/mediation-sessions/` | Online mediation room |
| `/settlements/` | Settlement records |
| `/digital-signatures/request/` | Digital signatures |
| `/payments/` | Payment & billing |
| `/subscriptions/` | Subscription plans |
| `/notifications/` | Notification center |
| `/grievances/` | Grievances & complaints |
| `/legal-compliance/` | Compliance dashboard |
| `/analytics/` | ODR analytics |
| `/ai-assistant/` | AI assistant features |
| `/admin-dashboard/` | Admin & super admin dashboard |
| `/mediator-portal/` | Mediator portal |
| `/legal-portal/` | Legal professional portal |
| `/business-portal/` | Business & corporate portal |
| `/admin/` | Django admin (superuser) |

## Tech Stack

- **Backend**: Django 6.1
- **Database**: SQLite (development) - swap to PostgreSQL for production
- **Frontend**: Bootstrap 5, vanilla JS, DataTables
- **Forms**: django-crispy-forms + crispy-bootstrap4
- **Auth**: Custom User model with email login, role-based permissions
- **Audit**: Middleware-driven audit logging on sensitive paths
- **File uploads**: 50 MB limit, secured per-dispute storage

## Production Considerations

For production deployment, swap the following:

1. **Database**: Replace SQLite with PostgreSQL or MySQL
2. **Web server**: Use Gunicorn or uWSGI behind Nginx
3. **Static files**: Serve via CDN or Nginx
4. **Media files**: Use S3/MinIO for file storage
5. **Caching**: Add Redis for sessions and caching
6. **Email**: Configure SMTP for transactional emails
7. **Payment gateway**: Integrate Razorpay/PayU for real payments
8. **Video**: Integrate WebRTC/Jitsi/Zoom for video mediation
9. **Async tasks**: Add Celery for background jobs (notifications, reminders)
10. **Realtime**: Add Django Channels for live messaging and session notifications
11. **Encryption**: Configure TLS, encrypt PII at rest
12. **Backup**: Schedule automated database backups

## License

This is a demo / reference implementation. Adapt as needed for your jurisdiction and use case.

---

Built as a comprehensive Django reference implementation covering all 22 feature areas of an Online Dispute Resolution platform.
