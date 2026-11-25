"""Disputes views - dispute registration and case filing (Section 2)."""
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView, CreateView, UpdateView, DetailView, TemplateView, View, FormView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponseForbidden, JsonResponse, HttpResponseRedirect
from django.db import transaction
from django.db.models import Q
from django import forms
from django.forms import formset_factory
from .models import Dispute, DisputeParty, DisputeTimelineEntry
from dispute_categories.models import DisputeCategory, DisputeEligibilityResult
from organizations.models import Organization
import uuid


class RoleRequiredMixin:
    """Mixin that checks user has one of the allowed roles."""

    allowed_roles = []

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if self.allowed_roles and request.user.role not in self.allowed_roles and not request.user.is_superuser:
            messages.error(request, "You don't have permission to access this page.")
            return redirect("dashboard:home")
        return super().dispatch(request, *args, **kwargs)


# ------------------------ Forms ------------------------


class DisputeForm(forms.ModelForm):
    """Comprehensive dispute registration form (Section 2)."""

    class Meta:
        model = Dispute
        fields = [
            "title",
            "description",
            "category",
            "sub_category",
            "disputed_amount",
            "currency",
            "is_amount_confidential",
            "agreement_reference",
            "agreement_date",
            "agreement_summary",
            "previous_communication_history",
            "requested_resolution",
            "jurisdiction",
            "location_of_dispute",
            "priority",
            "is_confidential",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 6}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "sub_category": forms.TextInput(attrs={"class": "form-control"}),
            "disputed_amount": forms.NumberInput(attrs={"class": "form-control"}),
            "currency": forms.Select(
                choices=[("INR", "INR ₹"), ("USD", "USD $"), ("EUR", "EUR €")],
                attrs={"class": "form-select"},
            ),
            "is_amount_confidential": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "agreement_reference": forms.TextInput(attrs={"class": "form-control"}),
            "agreement_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "agreement_summary": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "previous_communication_history": forms.Textarea(
                attrs={"class": "form-control", "rows": 4}
            ),
            "requested_resolution": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "jurisdiction": forms.TextInput(attrs={"class": "form-control"}),
            "location_of_dispute": forms.TextInput(attrs={"class": "form-control"}),
            "priority": forms.Select(attrs={"class": "form-select"}),
            "is_confidential": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class DisputePartyForm(forms.Form):
    """Invite additional parties to a dispute (Section 2)."""

    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    role = forms.ChoiceField(
        choices=[("respondent", "Respondent"), ("co_claimant", "Co-Claimant"),
                 ("co_respondent", "Co-Respondent"), ("third_party", "Third Party")],
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    contact_phone = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"class": "form-control"})
    )


# ------------------------ Views ------------------------


class DisputeListView(LoginRequiredMixin, ListView):
    """Centralized case dashboard (Section 4)."""

    template_name = "disputes/dispute_list.html"
    context_object_name = "disputes"
    paginate_by = 25

    def get_queryset(self):
        user = self.request.user
        qs = Dispute.objects.all()
        # Role-based filtering
        if user.role == "individual" or user.role == "claimant":
            qs = qs.filter(claimant=user)
        elif user.role == "respondent":
            qs = qs.filter(parties__user=user).distinct()
        elif user.role == "mediator":
            qs = qs.filter(assigned_mediator__user=user)
        elif user.role == "lawyer":
            qs = qs.filter(
                Q(representing_lawyer=user) |
                Q(parties__representing_lawyer=user)
            ).distinct()
        elif user.role == "business":
            qs = qs.filter(claimant=user)
        elif user.role in {"case_manager", "administrator", "super_admin"}:
            pass  # see all
        # Status filter
        status = self.request.GET.get("status")
        if status:
            qs = qs.filter(status=status)
        category_id = self.request.GET.get("category")
        if category_id:
            qs = qs.filter(category_id=category_id)
        return qs.order_by("-created_at")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["statuses"] = Dispute.Status.choices
        ctx["categories"] = DisputeCategory.objects.filter(is_active=True)
        ctx["status_filter"] = self.request.GET.get("status", "")
        ctx["category_filter"] = self.request.GET.get("category", "")
        return ctx


class DisputeCreateView(LoginRequiredMixin, CreateView):
    """Create new dispute case (Section 2)."""

    model = Dispute
    form_class = DisputeForm
    template_name = "disputes/dispute_create.html"

    def get_initial(self):
        initial = super().get_initial()
        initial["jurisdiction"] = "India"
        initial["currency"] = "INR"
        return initial

    def form_valid(self, form):
        with transaction.atomic():
            dispute = form.save(commit=False)
            dispute.claimant = self.request.user
            dispute.status = Dispute.Status.DRAFT
            dispute.is_draft = True
            # Determine priority from category
            dispute.priority = dispute.category.default_priority.upper()[:6].lower()
            dispute.save()

            # Auto-add claimant as a DisputeParty
            DisputeParty.objects.create(
                dispute=dispute,
                user=self.request.user,
                role=DisputeParty.PartyRole.CLAIMANT,
                invitation_status=DisputeParty.InvitationStatus.ACCEPTED,
                joined_at=timezone.now(),
                has_accepted_jurisdiction=True,
                has_signed_confidentiality=True,
            )

            # Timeline entry
            DisputeTimelineEntry.objects.create(
                dispute=dispute,
                entry_type=DisputeTimelineEntry.EntryType.CREATED,
                title="Dispute case created (draft)",
                description=f"Draft dispute '{dispute.title}' created by {self.request.user.email}",
                actor=self.request.user,
            )

        messages.success(
            self.request,
            f"Dispute case created as draft. Case reference: {dispute.case_ref}. "
            f"You can invite parties and add documents before submitting.",
        )
        return redirect("disputes:detail", pk=dispute.pk)


class DisputeDraftListView(LoginRequiredMixin, ListView):
    template_name = "disputes/dispute_drafts.html"
    context_object_name = "drafts"

    def get_queryset(self):
        return Dispute.objects.filter(
            claimant=self.request.user,
            is_draft=True,
            status=Dispute.Status.DRAFT,
        ).order_by("-created_at")


class DisputeDetailView(LoginRequiredMixin, DetailView):
    """Case detail view (Section 4)."""

    model = Dispute
    template_name = "disputes/dispute_detail.html"
    context_object_name = "dispute"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not self._user_can_access(obj):
            return HttpResponseForbidden("You do not have access to this dispute.")
        return obj

    def _user_can_access(self, dispute):
        user = self.request.user
        if user.is_superuser or user.role in {"administrator", "super_admin", "case_manager"}:
            return True
        if dispute.assigned_mediator and dispute.assigned_mediator.user == user:
            return True
        if dispute.claimant == user:
            return True
        if dispute.representing_lawyer == user:
            return True
        if dispute.parties.filter(user=user).exists():
            return True
        return False

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        dispute = self.object
        ctx["parties"] = dispute.parties.all()
        ctx["timeline"] = dispute.timeline_entries.all()[:30]
        ctx["documents"] = dispute.documents.all()[:10]
        ctx["payments"] = dispute.payments.all()
        ctx["scheduled_sessions"] = dispute.scheduled_sessions.all()
        ctx["proposals"] = dispute.settlement_proposals.all()[:10]
        ctx["settlement_records"] = dispute.settlement_records.all()
        ctx["threads"] = dispute.message_threads.all()
        ctx["invite_form"] = DisputePartyForm()
        ctx["can_submit"] = dispute.is_draft and dispute.parties.filter(
            role="respondent"
        ).exists()
        ctx["can_edit"] = dispute.claimant == self.request.user and dispute.is_draft
        return ctx


class DisputeEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Edit a draft dispute."""

    model = Dispute
    form_class = DisputeForm
    template_name = "disputes/dispute_edit.html"

    def test_func(self):
        obj = self.get_object()
        return obj.claimant == self.request.user and obj.is_draft

    def form_valid(self, form):
        messages.success(self.request, "Dispute draft updated.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("disputes:detail", kwargs={"pk": self.object.pk})


class DisputeSubmitView(LoginRequiredMixin, View):
    """Submit dispute application (Section 2)."""

    def post(self, request, pk):
        dispute = get_object_or_404(Dispute, pk=pk)
        if dispute.claimant != request.user and not request.user.is_superuser:
            return HttpResponseForbidden()
        if not dispute.is_draft:
            messages.error(request, "This dispute has already been submitted.")
            return redirect("disputes:detail", pk=pk)
        if not dispute.parties.filter(role="respondent").exists():
            messages.error(
                request,
                "Please invite at least one respondent before submitting.",
            )
            return redirect("disputes:detail", pk=pk)
        if not dispute.title or not dispute.description or not dispute.requested_resolution:
            messages.error(
                request, "Please complete title, description, and requested resolution."
            )
            return redirect("disputes:detail", pk=pk)

        dispute.status = Dispute.Status.SUBMITTED
        dispute.acknowledged_at = timezone.now()
        dispute.is_draft = False
        dispute.save()

        DisputeTimelineEntry.objects.create(
            dispute=dispute,
            entry_type=DisputeTimelineEntry.EntryType.SUBMITTED,
            title="Dispute application submitted",
            description=f"Submitted by {request.user.email}. Acknowledged at {dispute.acknowledged_at:%Y-%m-%d %H:%M}.",
            actor=request.user,
        )
        messages.success(
            request,
            f"Dispute {dispute.case_ref} submitted successfully! "
            f"An acknowledgement has been generated. You will be notified of further updates.",
        )
        return redirect("disputes:detail", pk=pk)


class DisputeWithdrawView(LoginRequiredMixin, View):
    """Case withdrawal (Section 4)."""

    def post(self, request, pk):
        dispute = get_object_or_404(Dispute, pk=pk)
        if dispute.claimant != request.user:
            return HttpResponseForbidden()
        if dispute.is_closed:
            messages.error(request, "Cannot withdraw a closed dispute.")
            return redirect("disputes:detail", pk=pk)
        reason = request.POST.get("reason", "").strip()
        if not reason:
            messages.error(request, "Please provide a reason for withdrawal.")
            return redirect("disputes:detail", pk=pk)
        dispute.status = Dispute.Status.WITHDRAWN
        dispute.closed_at = timezone.now()
        dispute.closure_reason = reason
        dispute.save()
        DisputeTimelineEntry.objects.create(
            dispute=dispute,
            entry_type=DisputeTimelineEntry.EntryType.CLOSURE,
            title="Case withdrawn by claimant",
            description=reason,
            actor=request.user,
        )
        messages.success(request, "Your dispute has been withdrawn.")
        return redirect("disputes:detail", pk=pk)


class InvitePartyView(LoginRequiredMixin, View):
    """Add multiple parties / party invitation (Section 2)."""

    def post(self, request, pk):
        dispute = get_object_or_404(Dispute, pk=pk)
        if dispute.claimant != request.user and not request.user.is_superuser:
            return HttpResponseForbidden()
        form = DisputePartyForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            role = form.cleaned_data["role"]
            # Find or create placeholder user
            from accounts.models import User
            try:
                party_user = User.objects.get(email__iexact=email)
            except User.DoesNotExist:
                party_user = User.objects.create_user(
                    email=email,
                    password=str(uuid.uuid4()),  # random pw - they must reset
                    first_name="Invited",
                    last_name="Party",
                    role=User.Role.RESPONDENT if role == "respondent" else User.Role.INDIVIDUAL,
                    is_active=False,  # will be activated when they accept invitation
                )
            if DisputeParty.objects.filter(dispute=dispute, user=party_user).exists():
                messages.warning(request, "This user is already a party to the dispute.")
            else:
                DisputeParty.objects.create(
                    dispute=dispute,
                    user=party_user,
                    role=role,
                    contact_email=email,
                    contact_phone=form.cleaned_data.get("contact_phone", ""),
                )
                DisputeTimelineEntry.objects.create(
                    dispute=dispute,
                    entry_type=DisputeTimelineEntry.EntryType.PARTY_INVITED,
                    title=f"Party invitation sent to {email}",
                    description=f"Invited as {role}",
                    actor=request.user,
                )
                messages.success(
                    request,
                    f"Invitation sent to {email}. They will need to register and accept.",
                )
        else:
            messages.error(request, "Invalid invitation form.")
        return redirect("disputes:detail", pk=pk)


class AcceptInvitationView(LoginRequiredMixin, View):
    """Accept party invitation (Section 2)."""

    def get(self, request, pk, token):
        dispute = get_object_or_404(Dispute, pk=pk)
        party = get_object_or_404(
            DisputeParty,
            dispute=dispute,
            invitation_token=token,
            invitation_status=DisputeParty.InvitationStatus.PENDING,
        )
        if party.user != request.user:
            return HttpResponseForbidden("This invitation is not for you.")
        return render(
            request,
            "disputes/accept_invitation.html",
            {"dispute": dispute, "party": party},
        )

    def post(self, request, pk, token):
        dispute = get_object_or_404(Dispute, pk=pk)
        party = get_object_or_404(
            DisputeParty,
            dispute=dispute,
            invitation_token=token,
        )
        if party.user != request.user:
            return HttpResponseForbidden()
        accepted = request.POST.get("accept") == "yes"
        if accepted:
            party.invitation_status = DisputeParty.InvitationStatus.ACCEPTED
            party.joined_at = timezone.now()
            party.has_accepted_jurisdiction = True
            party.has_signed_confidentiality = True
            party.save()
            DisputeTimelineEntry.objects.create(
                dispute=dispute,
                entry_type=DisputeTimelineEntry.EntryType.PARTY_ACCEPTED,
                title=f"{request.user.email} accepted invitation",
                actor=request.user,
            )
            messages.success(request, "You have joined the dispute.")
        else:
            party.invitation_status = DisputeParty.InvitationStatus.REJECTED
            party.save()
            DisputeTimelineEntry.objects.create(
                dispute=dispute,
                entry_type=DisputeTimelineEntry.EntryType.PARTY_REJECTED,
                title=f"{request.user.email} declined invitation",
                actor=request.user,
            )
            messages.info(request, "You have declined the invitation.")
        return redirect("disputes:detail", pk=pk)


class DisputeEligibilityView(LoginRequiredMixin, View):
    """Eligibility screening (Section 3)."""

    def get(self, request, pk):
        dispute = get_object_or_404(Dispute, pk=pk)
        questions = dispute.category.eligibility_questions.all()
        return render(
            request,
            "disputes/eligibility_screen.html",
            {"dispute": dispute, "questions": questions},
        )

    def post(self, request, pk):
        dispute = get_object_or_404(Dispute, pk=pk)
        questions = dispute.category.eligibility_questions.all()
        disqualifying_yes = 0
        answered = 0
        notes = []
        for q in questions:
            ans = request.POST.get(f"q_{q.id}")
            if ans:
                answered += 1
                if ans == "yes" and q.disqualifying_if_yes:
                    disqualifying_yes += 1
                    notes.append(f"Disqualifying answer: {q.question}")
        if answered == 0:
            messages.error(request, "Please complete the eligibility questionnaire.")
            return redirect("disputes:eligibility", pk=pk)

        # Compute decision
        score = int(((answered - disqualifying_yes) / max(answered, 1)) * 100)
        if disqualifying_yes > 0:
            decision = "ineligible"
            is_eligible = False
        elif score >= 75:
            decision = "eligible"
            is_eligible = True
        elif score >= 50:
            decision = "conditional"
            is_eligible = True
        else:
            decision = "pending"
            is_eligible = False

        result = DisputeEligibilityResult.objects.create(
            dispute=dispute,
            reviewed_by=request.user if request.user.is_staff else None,
            is_eligible=is_eligible,
            eligibility_score=score,
            notes="; ".join(notes),
            disqualifying_reasons="\n".join(notes),
            requires_human_review=True,
            decision=decision,
            reviewed_at=timezone.now() if decision != "pending" else None,
        )
        if decision == "eligible":
            dispute.status = Dispute.Status.ELIGIBLE_FOR_MEDIATION
            dispute.save()
            messages.success(request, f"Dispute eligible for mediation (score {score}%).")
        else:
            messages.warning(
                request,
                f"Eligibility decision: {decision} (score {score}%). A case manager will review.",
            )
        return redirect("disputes:detail", pk=pk)


class TrackApplicationStatusView(TemplateView):
    """Track application status (Section 2)."""

    template_name = "disputes/track_status.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ref = self.request.GET.get("case_ref", "").strip()
        if ref:
            try:
                dispute = Dispute.objects.get(case_ref=ref)
                ctx["dispute"] = dispute
                ctx["status_history"] = dispute.timeline_entries.all()
            except Dispute.DoesNotExist:
                ctx["error"] = f"No dispute found with reference {ref}."
        return ctx


class ChangeStatusView(LoginRequiredMixin, View):
    """Change dispute status (case manager/admin) (Section 4)."""

    def post(self, request, pk):
        dispute = get_object_or_404(Dispute, pk=pk)
        if request.user.role not in {"case_manager", "administrator", "super_admin"} and not request.user.is_superuser:
            return HttpResponseForbidden()
        new_status = request.POST.get("status")
        old_status = dispute.status
        if new_status in dict(Dispute.Status.choices):
            dispute.status = new_status
            dispute.save()
            DisputeTimelineEntry.objects.create(
                dispute=dispute,
                entry_type=DisputeTimelineEntry.EntryType.STATUS_CHANGE,
                title=f"Status changed: {old_status} → {new_status}",
                actor=request.user,
                description=request.POST.get("notes", ""),
            )
            messages.success(request, f"Status changed to {dispute.get_status_display()}.")
        return redirect("disputes:detail", pk=pk)


class AssignCaseManagerView(LoginRequiredMixin, View):
    """Case assignment (Section 4)."""

    def post(self, request, pk):
        dispute = get_object_or_404(Dispute, pk=pk)
        if request.user.role not in {"administrator", "super_admin"} and not request.user.is_superuser:
            return HttpResponseForbidden()
        manager_id = request.POST.get("case_manager_id")
        from accounts.models import User
        manager = get_object_or_404(User, pk=manager_id, role="case_manager")
        dispute.assigned_case_manager = manager
        dispute.save()
        DisputeTimelineEntry.objects.create(
            dispute=dispute,
            entry_type=DisputeTimelineEntry.EntryType.STATUS_CHANGE,
            title=f"Case manager assigned: {manager.email}",
            actor=request.user,
        )
        messages.success(request, f"Case manager {manager.email} assigned.")
        return redirect("disputes:detail", pk=pk)


class DisputeCloseView(LoginRequiredMixin, View):
    """Case closure (Section 4)."""

    def post(self, request, pk):
        dispute = get_object_or_404(Dispute, pk=pk)
        if request.user.role not in {"administrator", "super_admin", "case_manager"} and not request.user.is_superuser:
            return HttpResponseForbidden()
        reason = request.POST.get("closure_reason", "").strip()
        if not reason:
            messages.error(request, "Please provide a closure reason.")
            return redirect("disputes:detail", pk=pk)
        dispute.status = Dispute.Status.CLOSED
        dispute.closed_at = timezone.now()
        dispute.closure_reason = reason
        dispute.save()
        DisputeTimelineEntry.objects.create(
            dispute=dispute,
            entry_type=DisputeTimelineEntry.EntryType.CLOSURE,
            title="Case closed by administrator",
            description=reason,
            actor=request.user,
        )
        messages.success(request, "Case closed.")
        return redirect("disputes:detail", pk=pk)


class DisputeReopenView(LoginRequiredMixin, View):
    """Reopening requests (Section 4)."""

    def post(self, request, pk):
        dispute = get_object_or_404(Dispute, pk=pk)
        if not dispute.is_closed:
            messages.error(request, "Only closed disputes can be reopened.")
            return redirect("disputes:detail", pk=pk)
        reason = request.POST.get("reason", "").strip()
        if not reason:
            messages.error(request, "Please provide a reason.")
            return redirect("disputes:detail", pk=pk)
        from case_management.models import CaseReopeningRequest
        CaseReopeningRequest.objects.create(
            dispute=dispute,
            requested_by=request.user,
            reason=reason,
            requested_at=timezone.now(),
        )
        messages.success(
            request,
            "Reopening request submitted. An administrator will review.",
        )
        return redirect("disputes:detail", pk=pk)


class DisputeArchiveView(LoginRequiredMixin, View):
    """Case archive (Section 4)."""

    def post(self, request, pk):
        dispute = get_object_or_404(Dispute, pk=pk)
        if request.user.role not in {"administrator", "super_admin"} and not request.user.is_superuser:
            return HttpResponseForbidden()
        if not dispute.is_closed:
            messages.error(request, "Only closed disputes can be archived.")
            return redirect("disputes:detail", pk=pk)
        from case_management.models import CaseArchive
        dispute.is_archived = True
        dispute.archived_at = timezone.now()
        dispute.save()
        CaseArchive.objects.create(
            dispute=dispute,
            archived_by=request.user,
            archive_reason=request.POST.get("reason", "Auto-archive on closure"),
        )
        DisputeTimelineEntry.objects.create(
            dispute=dispute,
            entry_type=DisputeTimelineEntry.EntryType.CLOSURE,
            title="Case archived",
            actor=request.user,
        )
        messages.success(request, "Case archived.")
        return redirect("disputes:detail", pk=pk)


# Wire up names used by urls.py (imported via *)
dispute_list = DisputeListView.as_view()
dispute_create = DisputeCreateView.as_view()
dispute_draft_list = DisputeDraftListView.as_view()
dispute_detail = DisputeDetailView.as_view()
dispute_edit = DisputeEditView.as_view()
dispute_submit = DisputeSubmitView.as_view()
dispute_withdraw = DisputeWithdrawView.as_view()
dispute_timeline = DisputeDetailView.as_view()
dispute_parties = DisputeDetailView.as_view()
invite_party = InvitePartyView.as_view()
accept_invitation = AcceptInvitationView.as_view()
dispute_eligibility = DisputeEligibilityView.as_view()
change_status = ChangeStatusView.as_view()
assign_case_manager = AssignCaseManagerView.as_view()
dispute_close = DisputeCloseView.as_view()
dispute_reopen = DisputeReopenView.as_view()
dispute_archive = DisputeArchiveView.as_view()
track_application_status = TrackApplicationStatusView.as_view()
