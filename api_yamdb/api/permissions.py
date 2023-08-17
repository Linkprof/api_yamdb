from rest_framework import permissions


class IsAdminModeratorOwnerOrReadOnly(permissions.BasePermission):
    """
    Безопасные запросы разрешены для анонимных пользователей.
    Не безопасные разрешены авторизованному пользователю,
    админу, модератору или автору.
    """
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_moderator
                or request.user.is_admin)


class IsAdmin(permissions.BasePermission):
    """Права доступа для администратора и/или суперюзера"""

    def has_permission(self, request, view):
        return (
            # Если пользователь не авторизован,
            # он не проходит проверку is_admin
            # как реализовать без is_authenticated?
            request.user.is_authenticated and (
                request.user.is_admin or request.user.is_superuser
            )
        )


class ReadOrIsAdminOnly(permissions.BasePermission):
    """
    Безопасные запросы для анонимных пользователей.
    Не безопасные запросы разрешены только администратору и суперюзеру
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or (
                request.user.is_authenticated and (
                    request.user.is_admin or request.user.is_superuser
                )
            )
        )
