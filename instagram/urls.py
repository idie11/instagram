from users.views import UserView, FavoritesView, UserFavoritesView
from django.urls.conf import include
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_auth.views import LoginView
from rest_auth.registration.views import RegisterView
from posts.views import PostView, CommentView, LikesView, PostLikesView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signin', LoginView.as_view(), name='rest_login'),
    path('signup', RegisterView.as_view(), name='rest_register'),
    path('', PostView.as_view({'get': 'list'})),
    path('silk/', include('silk.urls', namespace='silk')),
    path('posts/create', PostView.as_view({'post': 'create'})),
    path('posts/<int:pk>/likes', PostLikesView.as_view()), 
    path('user/<int:pk>', UserView.as_view({'get':'retrieve', 'put': 'update'})),
    path('user/<int:pk>/favorites', UserFavoritesView.as_view()),
    path('comment/', CommentView.as_view({'post':'create'})),
    path('comment/<int:pk>', CommentView.as_view({'put':'update', 'delete': 'destroy'})),
    path('like/<int:pk>', LikesView.as_view()), 
    path('favorites/<int:pk>', FavoritesView.as_view()),
]
    
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    