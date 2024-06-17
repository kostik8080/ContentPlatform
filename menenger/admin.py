from django.contrib import admin

from menenger.models import Content, Like


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    pass

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass
