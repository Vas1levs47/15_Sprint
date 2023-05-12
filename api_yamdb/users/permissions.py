from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Административно-управленческий персонал."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin
                or request.user.is_staff
                or request.user.is_superuser)
