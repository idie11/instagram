from users.models import User
from django.db.models import fields
from rest_framework import serializers
from posts.models import Comments, Post, PostImage, Likes

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'avatar')


class CommentsSerializers(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Comments
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        comment = Comments.objects.create(owner=user, **validated_data)
        return comment

    def update(self, instance, validated_data):
        data = validated_data.copy()
        data.pop('post', None)
        for attr, value, in data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance        
   

class PostImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostImage
        fields =('id', 'image')


class PostSerializer(serializers.ModelSerializer):
    post_image = PostImageSerializer(many=True, read_only=True)
    # owner_nick_name = serializers.CharField(read_only=True)
    # owner_avatar = serializers.SerializerMethodField(read_only=True)
    owner = UserSerializer(many=False, read_only=True)
    post_comments = CommentsSerializers(many=True, read_only=True)
    likes_count = serializers.IntegerField()
    class Meta:
        model = Post
        fields = ('id','owner', 'text', 'date', 'post_image', 'post_comments','likes_count')

    # def get_owner_avatar(self, obj):
    #     return f"http://{self.context.get('request').META['HTTP_HOST']}/media/{obj.owner_avatar}"

    def create(self, validated_data):
        user = self.context.get('request').user
        post = Post.objects.create(owner=user, **validated_data)
        images = self.context.get('request').data.getlist('post_image')
        for i in images:
            PostImage.objects.create(images=i, post=post)
        return post

    def update(self, instance, validated_data):
        for attr, value, in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        images = self.context.get('request').data.getlist('post_image')
        if images:
            PostImage.objects.filter(post=instance).delete()
            # images_list =[]
            # for i in images:
                # images_list += PostImage(image=i,post=instance)
            # PostImage.objects.create(images=i, post=instance)
            images_list = [PostImage(image=i, post=instance) for i in images]
        return instance
        
# class LikeSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Likes
#         fields = '__all__'
    