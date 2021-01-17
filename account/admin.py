from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import user

# Register your models here.

class customUA(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username',)}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }), 
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'username', 'is_staff')
    search_fields = ('username', 'email')
    ordering = ('email',)

admin.site.register(user, customUA)
