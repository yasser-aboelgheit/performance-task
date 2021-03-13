from rest_framework.permissions import BasePermission

class IsNotSuperUserButStaff(BasePermission):
    """
    Allows access only to admin users who are not superusers.
    """

    def has_permission(self, request, view):
        return bool(request.user.is_staff and not request.user.is_superuser)
