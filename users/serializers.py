from rest_framework import serializers
from posts.serializers import PostImageSerializer
from posts.models import Post
from .models import User


class PostForUserSerializer(serializers.ModelSerializer):
    post_image = PostImageSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id','owner', 'text', 'date', 'post_image')


class UserSerializer(serializers.ModelSerializer):
    post_owner = PostForUserSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('phone_number', 'site', 'bio', 'avatar', 'username', 'first_name', 'last_name', 'email', 'post_owner')

