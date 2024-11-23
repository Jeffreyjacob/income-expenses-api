from django.urls import path
from authentication import views as api_view
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("user/register/",api_view.RegisterView.as_view(),name='register'),
    path("email-verify/",api_view.VerifyEmail.as_view(),name="email-verify"),
    path("user/login/",api_view.LoginAPIView.as_view(),name="login"),
    path("user/token/refresh/",TokenRefreshView.as_view(),name="refresh-token"),
    path("request-reset-email/",api_view.RequestPasswordResetEmail.as_view(),name='request-reset-email'),
    path("password-reset/<uidb64>/<token>/",api_view.PasswordTokenCheckApi.as_view(),name="password-reset-confirm"),
    path("set-new-password/",api_view.SetNewPasswordAPIView.as_view(),name="set-new-password")
]