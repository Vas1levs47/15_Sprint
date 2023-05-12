from rest_framework.permissions import (SAFE_METHODS, BasePermission,
                                        IsAuthenticatedOrReadOnly)


class AdminOrReadOnly(BasePermission):
    """Доступ к изменению у Админа и СуперАдмина, либо чтение."""

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or (request.user.is_authenticated
                    and (request.user.is_admin or request.user.is_superuser)))


class AuthorModerOrRead(IsAuthenticatedOrReadOnly):
    """Доступ к изменению у Автора и Персонала, либо чтение."""

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or obj.author == request.user or request.user.is_moderator
                or request.user.is_admin or request.user.is_superuser)
