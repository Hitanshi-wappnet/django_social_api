from django.urls import path
from UserProfile import views

urlpatterns = [
    path("viewprofile/", views.UserProfileView.as_view(), name='viewprofile'),
    path("updateprofile/<int:pk>/", views.UserProfileView.as_view(),
         name='updateprofile'),
    path("deleteprofile/<int:pk>/", views.UserProfileView.as_view(),
         name="resetpassword"),
    path("changepassword/", views.ChangePasswordView.as_view(),
         name='changepassword'),
]
