from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_name', 'last_name', 'email', 'phone', 'role', 'is_active',)
    list_filter = ('is_active', 'role',)
    search_fields = ('email', 'phone',)
