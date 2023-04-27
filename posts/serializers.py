from rest_framework import serializers
from posts.models import Post
from posts.models import Like
from posts.models import Comment


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

    def validate(self, data):
        user = data['user']
        post = data['post']
        if Like.objects.filter(user=user, post=post).exists():
            raise serializers.ValidationError('You already liked this post')
        return data


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
