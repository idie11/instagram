from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsUserOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        print(1)
        if request.method == 'GET':
            return True 
        return obj == request.user