from django.contrib import admin
from posts.models import Post, Like, Comment


# Registation of Forget Password Model
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'content', 'image',
                    'video', 'total_likes', 'total_comments']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post', 'created_at', 'updated_at', 'likes']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post', 'comment',
                    'created_at', 'updated_at', 'count_comment']
