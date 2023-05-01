from django.urls import path
from authentication import views

urlpatterns = [
     path("register/", views.RegisterView.as_view(), name='register'),

     path("resend_otp_registration/",
          views.ResendOtpUserActivationView.as_view(),
          name='register'),

     path("verifyotp_registration/",
          views.VerifyUserActivationOtpView.as_view(),
          name='verifyotp_registration'),

     path("login/", views.LoginView.as_view(), name='login'),

     path("forgetpassword/", views.ForgetPasswordView.as_view(),
          name="resetpassword"),

     path("resend_otp_forgetpassword/",
          views.ResendOtpForgetPasswordView.as_view(),
          name='resend_otp_forgetpassword'),

     path("resetpassword/", views.ResetPasswordView.as_view(),
          name="resetpassword"),

     path("verifyotp/", views.VerifyOtpView.as_view(), name='verifyotp'),

     path("logout/", views.LogoutView.as_view(), name='logout')
]
