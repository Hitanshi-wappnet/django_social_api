from rest_framework import serializers
from SocialUser.models import Follow, Message


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'

    def validate(self, data):
        follower = data['follower']
        following = data['following']
        if Follow.objects.filter(follower=follower, following=following).exists():
            raise serializers.ValidationError('You already following this user')
        return data


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
