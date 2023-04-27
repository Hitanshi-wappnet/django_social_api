from django.urls import path
from authentication import views

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name='register'),
    path("login/", views.LoginView.as_view(), name='login'),
    path("forgetpassword/", views.ForgetPasswordView.as_view(),
         name="resetpassword"),
    path("resetpassword/", views.ResetPasswordView.as_view(),
         name="resetpassword"),
    path("verifyotp/", views.VerifyOtpView.as_view(), name='verifyotp'),
    path("logout/", views.LogoutView.as_view(), name='logout')
]
