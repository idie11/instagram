from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsPostOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        return obj.owner == request.user


class IsCommentOwnerOrReadOly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        elif request.method == 'DELETE':
            return obj.owner == request.user or obj.post.owner == request.user
        return obj.owner == request.user
