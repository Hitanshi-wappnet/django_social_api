from rest_framework import serializers
from posts.models import Post, Hashtag
from posts.models import Like
from posts.models import Comment
import re


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'user', 'content', 'image',
                  'video', 'total_likes', 'total_comments']

    def save(self, **kwargs):

        # Find all hashtags in the content
        hashtags = re.findall(r'\B#\w*[a-zA-Z]+\w*', self.validated_data.get('content', ''))

        # Call the parent `save` method to save the post instance
        post_instance = super().save(**kwargs)

        # Remove any duplicate hashtags
        hashtags = list(set(hashtags))
        # Create a new Hashtag object for each hashtag
        for hashtag in hashtags:
            name = hashtag[1:]
            hashtag_obj = Hashtag.objects.get_or_create(name=name)[0]

            # Add the hashtag to the post's hashtags field
            post_instance.hashtags.add(hashtag_obj)
        return post_instance


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
