from django.urls import path
from posts import views

urlpatterns = [
    path('addpost/', views.PostView.as_view(), name='addpost'),
    path('search/', views.PostSearchView.as_view(), name='search'),
    path('like/<int:pk>/', views.LikeView.as_view(), name='like'),
    path('comment/<int:pk>/', views.CommentView.as_view(), name='comment')
]
