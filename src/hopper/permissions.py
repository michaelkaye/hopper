from rest_framework import permissions

class EventAccessPermission(permissions.BasePermission):
    message = "Object is not public or you are not an admin"
    def has_object_permission(self, request, view, object):
        if request.method in permissions.SAFE_METHODS:
            if object.public:
                return True

        if request.user.is_authenticated:
            return True

        return False

     
