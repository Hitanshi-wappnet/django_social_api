from django.urls import path
from posts import views

urlpatterns = [
    path('addpost/', views.PostView.as_view(), name='addpost'),
    path('viewpost_user/', views.UserPostSearchView.as_view(), 
         name='viewpost'),
    path('display_posts/', views.PostListView.as_view(), name='search'),
    path('search/<str:query>/', views.PostSearchView.as_view(), name='search'),
    path('hashtagsearch/<str:search>/', views.HashtagSearchView.as_view(),
         name='Hahtagsearch'),
    path('like/<int:pk>/', views.LikeView.as_view(), name='like'),
    path('comment/<int:pk>/', views.CommentView.as_view(), name='comment'),
    path('deletepost/<int:pk>/', views.PostView.as_view(),
         name='deletepost'),
    path('trending/', views.TrendingPostView.as_view(), name='trending_post')
]
