from django.contrib import admin
from .models import Admin


@admin.register(Admin)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']
    search_fields = ['user__username']
