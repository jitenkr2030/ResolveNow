"""
Accounts views, forms, signals, and context processor.
"""
from django import forms
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, TemplateView, ListView
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponseForbidden, JsonResponse
from .models import User, LoginHistory, AccountDeletionRequest
import user_agents
import socket


# ------------------------ Forms ------------------------


class UserRegistrationForm(forms.ModelForm):
    """Multi-role registration form (Section 1).

    Supports individual, business, lawyer, mediator registration.
    """

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Create a strong password"}
        ),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Repeat password"}
        ),
    )
    consent_terms = forms.BooleanField(
        required=True,
        label="I agree to the Terms of Service and Privacy Policy.",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )
    consent_whatsapp = forms.BooleanField(
        required=False,
        label="I consent to receive updates via WhatsApp.",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "preferred_language",
        )
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "role": forms.Select(attrs={"class": "form-select"}),
            "preferred_language": forms.Select(
                choices=[
                    ("English", "English"),
                    ("Hindi", "Hindi"),
                    ("Tamil", "Tamil"),
                    ("Telugu", "Telugu"),
                    ("Kannada", "Kannada"),
                    ("Bengali", "Bengali"),
                    ("Marathi", "Marathi"),
                    ("Gujarati", "Gujarati"),
                    ("Malayalam", "Malayalam"),
                    ("Punjabi", "Punjabi"),
                ],
                attrs={"class": "form-select"},
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Restrict role choices on the public registration form
        self.fields["role"].choices = [
            (User.Role.INDIVIDUAL, "Individual"),
            (User.Role.BUSINESS, "Business User"),
            (User.Role.LAWYER, "Lawyer / Legal Professional"),
            (User.Role.MEDIATOR, "Mediator"),
        ]

    def clean_email(self):
        email = self.cleaned_data["email"].lower().strip()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean_password2(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match.")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.username = None
        user.consent_terms_of_service = True
        user.consent_privacy_policy = True
        user.consent_whatsapp = self.cleaned_data.get("consent_whatsapp", False)
        user.consent_timestamp = timezone.now()
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    """Profile management form (Section 1)."""

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "phone_number",
            "alternate_phone",
            "date_of_birth",
            "address_line1",
            "address_line2",
            "city",
            "state",
            "postal_code",
            "country",
            "preferred_language",
            "timezone_preference",
            "consent_marketing",
            "consent_whatsapp",
        )


class LoginForm(forms.Form):
    """Login form compatible with LoginView's request kwarg."""

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "autofocus": True})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        from django.contrib.auth import authenticate

        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        if email and password:
            self.user_cache = authenticate(self.request, username=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Invalid email or password.")
            if not self.user_cache.is_active:
                raise forms.ValidationError("This account is inactive.")
        return self.cleaned_data

    def get_user(self):
        return self.user_cache


# ------------------------ Views ------------------------


class ResolveNowLoginView(LoginView):
    """Custom login view with login history tracking."""

    template_name = "registration/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super().form_valid(form)
        self._record_login(self.request.user, success=True)
        if self.request.user.is_suspended:
            from django.contrib.auth import logout

            logout(self.request)
            messages.error(
                self.request,
                "Your account has been suspended. Please contact support.",
            )
            return redirect("accounts:login")
        messages.success(self.request, f"Welcome back, {self.request.user.first_name}!")
        return response

    def form_invalid(self, form):
        email = form.cleaned_data.get("email")
        if email:
            try:
                user = User.objects.get(email__iexact=email)
                self._record_login(user, success=False)
            except User.DoesNotExist:
                pass
        messages.error(self.request, "Invalid email or password.")
        return super().form_invalid(form)

    def _record_login(self, user, success):
        ua_string = self.request.META.get("HTTP_USER_AGENT", "")
        xff = self.request.META.get("HTTP_X_FORWARDED_FOR")
        ip = (xff.split(",")[0] if xff else None) or self.request.META.get(
            "REMOTE_ADDR"
        )
        try:
            ua = user_agents.parse(ua_string)
            device = (
                "mobile" if ua.is_mobile else "tablet" if ua.is_tablet else "desktop"
            )
            browser = ua.browser.family
            os_name = ua.os.family
        except Exception:
            device, browser, os_name = "", "", ""
        LoginHistory.objects.create(
            user=user,
            ip_address=ip,
            user_agent=ua_string,
            device_type=device,
            browser=browser,
            os=os_name,
            is_successful=success,
            session_key=self.request.session.session_key or "",
        )
        if success:
            user.last_login_ip = ip
            user.failed_login_attempts = 0
            user.save(update_fields=["last_login_ip", "failed_login_attempts"])
        else:
            user.failed_login_attempts += 1
            user.last_failed_login = timezone.now()
            user.save(update_fields=["failed_login_attempts", "last_failed_login"])


class RegisterView(SuccessMessageMixin, CreateView):
    """Multi-role registration (Section 1)."""

    template_name = "registration/register.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("accounts:login")
    success_message = "Your account has been created. Please verify your email to continue."

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        # Send email verification
        try:
            send_mail(
                subject="Welcome to ResolveNow - Verify your email",
                message=(
                    f"Hi {user.first_name},\n\n"
                    f"Welcome to ResolveNow. Please verify your email by clicking "
                    f"the link below:\n\n"
                    f"http://{self.request.get_host()}/accounts/verify-email/{user.email_verification_token}/\n\n"
                    f"Regards,\nResolveNow Team"
                ),
                from_email="noreply@resolvenow.in",
                recipient_list=[user.email],
                fail_silently=True,
            )
        except Exception:
            pass
        # Auto-create related profile based on role
        from user_profiles.models import UserProfile
        from organizations.models import Organization

        UserProfile.objects.get_or_create(user=user)
        if user.role == User.Role.BUSINESS:
            # Prompt to create org
            messages.info(
                self.request,
                "Please complete your business registration in your dashboard.",
            )
        elif user.role == User.Role.MEDIATOR:
            messages.info(
                self.request,
                "Please complete your mediator professional profile after verifying your email.",
            )
        return response


def verify_email(request, token):
    try:
        user = User.objects.get(email_verification_token=token)
        user.is_email_verified = True
        user.email_verification_token = ""
        user.save(update_fields=["is_email_verified", "email_verification_token"])
        messages.success(request, "Your email has been verified. Please log in.")
        return redirect("accounts:login")
    except User.DoesNotExist:
        messages.error(request, "Invalid or expired verification link.")
        return redirect("accounts:login")


class ProfileView(LoginRequiredMixin, UpdateView):
    """Profile management (Section 1)."""

    model = User
    form_class = UserProfileForm
    template_name = "accounts/profile.html"
    success_url = reverse_lazy("accounts:profile")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Your profile has been updated.")
        return super().form_valid(form)


class LoginHistoryView(LoginRequiredMixin, ListView):
    """Login history and device management (Section 1)."""

    template_name = "accounts/login_history.html"
    context_object_name = "logins"
    paginate_by = 25

    def get_queryset(self):
        return LoginHistory.objects.filter(user=self.request.user)


class AccountDashboardView(LoginRequiredMixin, TemplateView):
    """Landing dashboard after login - routes based on role."""

    template_name = "accounts/account_dashboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["user"] = self.request.user
        return ctx


# ------------------------ Signal: send welcome email ------------------------


@receiver(post_save, sender=User)
def create_user_profile_signal(sender, instance, created, **kwargs):
    if created:
        from user_profiles.models import UserProfile

        UserProfile.objects.get_or_create(user=instance)


# ------------------------ Context processor for role-based UI ------------------------


def user_role_context(request):
    if hasattr(request, "user") and request.user.is_authenticated:
        return {
            "current_user_role": request.user.role,
            "current_user_display_role": request.user.get_role_display(),
            "is_mediator_user": request.user.is_mediator,
            "is_lawyer_user": request.user.is_lawyer,
            "is_business_user": request.user.is_business_user,
            "is_staff_user": request.user.is_staff_member,
            "is_admin_user": request.user.is_admin_level,
        }
    return {}
