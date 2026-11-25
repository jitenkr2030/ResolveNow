from django.urls import path
from verification.views import *

app_name = "verification"

urlpatterns = [
    path("", verification_dashboard, name="dashboard"),
    path("submit/", verification_submit, name="submit"),
    path("kyc/", kyc_submit, name="kyc"),
    path("otp/send/", otp_send, name="otp_send"),
    path("otp/verify/", otp_verify, name="otp_verify"),
    path("admin/", verification_admin_list, name="admin_list"),
    path("<int:pk>/review/", verification_review, name="review"),
]
