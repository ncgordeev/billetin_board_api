from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
    """Проверка прав на владельца, администратора"""
    message = "Доступно только владельцу или администратору!"

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (request.user == obj or request.user.is_superuser)


class IsAutor(BasePermission):
    """Проверка на автора, администратора объявления, комментария"""
    message = "Доступно только автору или администратору!"

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (request.user == obj.author or request.user.is_superuser)
