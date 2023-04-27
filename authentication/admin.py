from django.contrib import admin
from authentication.models import VerifyOtp
from authentication.models import User


# Registation of Forget Password Model
@admin.register(VerifyOtp)
class VerifyOtpAdmin(admin.ModelAdmin):
    fields = ["user", "otp"]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "username" ,"first_name", "last_name",
                    "bio", "birth_date", "followers", "following"]
