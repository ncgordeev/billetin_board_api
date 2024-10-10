from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
    """Проверка прав на владельца, администратора"""
    message = "Доступ запрещен! Данное действие доступно владельцу или администратору!"

    def has_object_permission(self, request, view, obj):
        return request.user == obj or request.user.is_superuser


class IsAutor(BasePermission):
    """Проверка на автора, администратора объявления, комментария"""
    message = "Доступ запрещен! Данное действие доступно автору или администратору!"

    def has_object_permission(self, request, view, obj):
        return request.user == obj.author or request.user.is_superuser
