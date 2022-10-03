'''
Django admin customization.
'''
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from core import models


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    ''' Define the admin pages for users. '''
    ordering = ['id']
    list_display = ['email', 'name', 'last_login']
    fieldsets = (
        (None, {'fields': ('name', 'email', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff',
                                       'is_superuser',)}),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {'classes': ('wide'),
                'fields': ('email', 'password1', 'password2',
                           'name', 'is_active', 'is_staff', 'is_superuser',)}),
    )


@admin.register(models.Profile)
class UserProfileAdmin(admin.ModelAdmin):
    ''' Define the admin pages for profiles. '''
    ordering = ['id']
    readonly_fields = ['user']

    # This will help you to disable add functionality
    def has_add_permission(self, request):
        return False

    # This will help you to disable delete functionality
    def has_delete_permission(self, request, obj=None):
        return False
