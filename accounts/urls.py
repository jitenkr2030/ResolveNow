from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.ResolveNowLoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(next_page="accounts:login"), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("verify-email/<str:token>/", views.verify_email, name="verify_email"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("login-history/", views.LoginHistoryView.as_view(), name="login_history"),
    path("dashboard/", views.AccountDashboardView.as_view(), name="account_dashboard"),
]
