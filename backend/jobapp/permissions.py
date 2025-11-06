from rest_framework  import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # You should return true!!!

        # read-only is allowed
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
