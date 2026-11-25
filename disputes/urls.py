from django.urls import path
from disputes.views import *

app_name = "disputes"

urlpatterns = [
    path("", dispute_list, name="list"),
    path("create/", dispute_create, name="create"),
    path("draft/", dispute_draft_list, name="drafts"),
    path("<int:pk>/", dispute_detail, name="detail"),
    path("<int:pk>/edit/", dispute_edit, name="edit"),
    path("<int:pk>/submit/", dispute_submit, name="submit"),
    path("<int:pk>/withdraw/", dispute_withdraw, name="withdraw"),
    path("<int:pk>/timeline/", dispute_timeline, name="timeline"),
    path("<int:pk>/parties/", dispute_parties, name="parties"),
    path("<int:pk>/invite-party/", invite_party, name="invite_party"),
    path("<int:pk>/accept-invite/<token>/", accept_invitation, name="accept_invitation"),
    path("<int:pk>/eligibility/", dispute_eligibility, name="eligibility"),
    path("<int:pk>/change-status/", change_status, name="change_status"),
    path("<int:pk>/assign-manager/", assign_case_manager, name="assign_manager"),
    path("<int:pk>/close/", dispute_close, name="close"),
    path("<int:pk>/reopen/", dispute_reopen, name="reopen"),
    path("<int:pk>/archive/", dispute_archive, name="archive"),
    path("track/", track_application_status, name="track_status"),
]
