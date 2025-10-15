from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Client

@admin.register(Client)
class ClientAdmin(UserAdmin):
    model = Client
    list_display = ('username', 'email', 'phone', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'email', 'phone')
    ordering = ('username',)
