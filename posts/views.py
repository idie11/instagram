from posts.serializers import CommentsSerializers, PostSerializer
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from posts.serializers import PostSerializer
from posts.models import Comments, Post, Likes
from django.db.models import F, Count
from .permissions import IsCommentOwnerOrReadOly, IsPostOwnerOrReadOnly
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response




class PostLikesView(APIView):

    def get(self, request, pk):
        post = Post.objects.get(id=pk)
        likes = Likes.objects.values_list('user__username', flat=True).filter(post=post)
        return Response(likes)


class LikesView(APIView):

    def get(self, request, pk):
        user = request.user
        post = Post.objects.get(id=pk)
        if Likes.objects.filter(user=user, post=post).exists():
            Likes.objects.filter(user=user, post=post).delete()
            return Response('Like Deleted', status=status.HTTP_201_CREATED)
        else:
            Likes.objects.create(user=user, post=post)
            return Response('Like created', status=status.HTTP_200_OK)


class PostView(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.prefetch_related('post_image', 'post_comments').annotate(
        owner_nick_name=F('owner__username'),
        owner_avatar=F('owner__avatar'),
        likes_count=Count('post_likes')
    ).order_by('-date')
    lookup_field = 'pk'
    permission_classes = (IsPostOwnerOrReadOnly,)

    def get_object(self):
        obj = Post.objects.prefetch_related('post_image').annotate(
            owner_nick_name=F('owner__username'),
            owner_avatar=F('owner__avatar'),
            likes_count=Count('post_likes')

        ).get(id=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj
        

class CommentView(ModelViewSet):
    serializer_class = CommentsSerializers
    queryset = Comments.objects.all()
    lookup_field ='pk'
    permission_classes = (IsCommentOwnerOrReadOly, )
