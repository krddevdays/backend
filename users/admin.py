from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Company


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        ('', {'fields': (('email', 'username'), 'password', ('first_name', 'last_name'), ('work', 'position'))}),
        ('Permissions', {'fields': (('is_active', 'is_staff', 'is_superuser'), 'groups', 'user_permissions')}),
        ('Dates', {'fields': (('date_joined', 'last_login'), )}),
    )


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    fieldsets = (
        ('', {'fields': (('title', 'status', 'owner'), 'description', ('address', 'coordinates'), ('site', 'phone', 'email'))}),
    )
