'''
Django admin customization.
'''
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from core import models
from django.contrib.contenttypes.admin import GenericTabularInline


class UserProfileInline(admin.StackedInline):
    ''' Define the admin pages for profiles. '''
    model = models.Profile


class LikesInline(GenericTabularInline):
    model = models.Likes


class CommentsInline(GenericTabularInline):
    model = models.Comments
    extra = 0
    readonly_fields = ['user', 'content']


@admin.register(models.Artist)
class ArtistAdmin(admin.ModelAdmin):
    ''' Define the admin pages for artists. '''
    ordering = ['id']
    list_display = ['name', 'country']


@admin.register(models.Contest)
class ContestAdmin(admin.ModelAdmin):
    ''' Define the admin pages for artists. '''
    ordering = ['id']
    list_display = ['name', 'organizer']
    inlines = [LikesInline, CommentsInline]


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    ''' Define the admin pages for users. '''
    ordering = ['id']
    list_display = ['email', 'name', 'last_login']
    inlines = [UserProfileInline]
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
