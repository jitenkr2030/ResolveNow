"""
Django settings for resolvenow_config project.

ResolveNow - Online Dispute Resolution (ODR) Platform
"""
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-resolvenow-odr-platform-development-key-change-in-production",
)

DEBUG = True
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "crispy_forms",
    "crispy_bootstrap4",
    # ResolveNow apps
    "accounts",
    "organizations",
    "user_profiles",
    "verification",
    "disputes",
    "case_management",
    "dispute_categories",
    "negotiation",
    "messaging",
    "documents",
    "mediators",
    "mediator_assignment",
    "scheduling",
    "mediation_sessions",
    "settlements",
    "digital_signatures",
    "payments",
    "subscriptions",
    "notifications",
    "grievances",
    "legal_compliance",
    "audit_logs",
    "analytics",
    "ai_assistant",
    # Aggregate portal / dashboard view apps
    "core_dashboards",
    "admin_dashboards",
    "mediator_portals",
    "legal_portals",
    "business_portals",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "audit_logs.middleware.AuditLogMiddleware",
]

ROOT_URLCONF = "resolvenow_config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "accounts.context_processors.user_role_context",
            ],
        },
    },
]

WSGI_APPLICATION = "resolvenow_config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
     "OPTIONS": {"min_length": 8}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "accounts.User"

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"

LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/dashboard/"
LOGOUT_REDIRECT_URL = "/accounts/login/"

# Session security
SESSION_COOKIE_AGE = 8 * 60 * 60  # 8 hours
SESSION_SAVE_EVERY_REQUEST = True

# File upload limits
FILE_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024  # 50 MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024

# Email (console backend for development)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "noreply@resolvenow.in"

# ResolveNow platform configuration
RESOLVENOW_CONFIG = {
    "PLATFORM_NAME": "ResolveNow",
    "TAGLINE": "Resolve Disputes Online. Fairly. Efficiently.",
    "SUPPORT_EMAIL": "support@resolvenow.in",
    "GRIEVANCE_EMAIL": "grievances@resolvenow.in",
    "CASE_REF_PREFIX": "RN",
    "CURRENCY": "INR",
    "CURRENCY_SYMBOL": "₹",
    "DEFAULT_CASE_FEE": 1500.00,
    "DEFAULT_MEDIATOR_FEE_PER_HOUR": 2500.00,
    "MIN_DISPUTED_AMOUNT": 1000.00,
    "MAX_DISPUTED_AMOUNT": 50000000.00,  # 5 crore
    "RESPONSE_DEADLINE_DAYS": 15,
    "NEGOTIATION_DEADLINE_DAYS": 30,
    "MEDIATION_SESSION_DEFAULT_DURATION_MINUTES": 90,
}
