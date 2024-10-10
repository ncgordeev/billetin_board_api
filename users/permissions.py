from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Проверка прав на владельца"""
    message = "Вы не владелец!"

    def has_object_permission(self, request, view, obj):
        return request.user == obj


class IsAutor(BasePermission):
    """Проверка на автора объявления, комментария"""
    message = "Вы не автор!"

    def has_object_permission(self, request, view, obj):
        return request.user == obj.author
