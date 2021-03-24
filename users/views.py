from users.serializers import UserSerializer
from rest_framework.viewsets import ModelViewSet
from .models import User,Favorites
from .permissions import IsUserOwnerOrReadOnly
from rest_framework.views import APIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from posts.models import Post



class UserView(ModelViewSet):
    queryset = User.objects.prefetch_related('post_owner')
    serializer_class = UserSerializer
    lookup_field = 'pk'
    permission_classes = (IsUserOwnerOrReadOnly,)
    


class UserFavoritesView(APIView):

    def get(self, request, pk):
        user = User.objects.get(id=pk)
        favorites = Favorites.objects.values_list('post__text', flat=True).filter(user=user)
        return Response(favorites)

class FavoritesView(APIView):

    def get(self, request, pk):
        user = request.user
        post = Post.objects.get(id=pk)
        if Favorites.objects.filter(user=user, post=post).exists():
            Favorites.objects.filter(user=user, post=post).delete()
            return Response('Favorite Deleted', status=status.HTTP_201_CREATED)
        else:
            Favorites.objects.create(user=user, post=post)
            return Response('Favorite Create', status=status.HTTP_200_OK)