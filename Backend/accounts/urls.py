from django.urls import path

from .views import LoginView, LogoutView, MeView, RefreshView, RegisterView, ResetPasswordView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("refresh/", RefreshView.as_view(), name="token_refresh"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset_password"),
    path("me/", MeView.as_view(), name="me"),
]
