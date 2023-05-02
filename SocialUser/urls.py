from django.urls import path
from SocialUser import views

urlpatterns = [
     path("follow/<int:pk>/", views.FollowUserView.as_view(), name="follow"),
     path("unfollow/<int:pk>/", views.UnfollowUserView.as_view(),
          name="unfollow"),
     path("sendmessage/<int:pk>/", views.SendMessageView.as_view(),
          name="sendmessage"),
     path("receivemessage/<int:pk>/", views.ReceiveMessageView.as_view(),
          name="receivemessage"),
     path("receivemessage/<int:pk>/", views.ReceiveMessageView.as_view(),
          name="receivemessage"),
     path("viewmessages/<int:pk>/", views.ListMessageView.as_view(),
          name="viewmessage"),
     path("trending/", views.TrendingUserView.as_view(), name="trending_user")
     # path("ws/chat/<int:pk>/", consumer.ChatConsumer.as_asgi(), name="chat"),
]
