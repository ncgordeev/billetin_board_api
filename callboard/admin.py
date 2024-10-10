from django.contrib import admin

from callboard.models import Ad, Review


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'price', 'author', 'created_at',)
    list_filter = ('author',)
    search_fields = ('title',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'ad', 'author', 'created_at',)
    list_filter = ('ad', 'author',)
    search_fields = ('ad',)
