from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        ('', {'fields': (('email', 'username'), 'password', ('first_name', 'last_name'))}),
        ('Permissions', {'fields': (('is_active', 'is_staff', 'is_superuser'), 'groups', 'user_permissions')}),
        ('Dates', {'fields': (('date_joined', 'last_login'), )}),
    )
