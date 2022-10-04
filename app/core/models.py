'''
Database models.
'''
import uuid
import os

from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django_countries.fields import CountryField
from ckeditor.fields import RichTextField
from django.dispatch import receiver
from django.db.models.signals import post_save


def avatar_image_file_path(instance, filename):
    ''' Generate file path for new recipe image. '''
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'avatar', filename)


class UserManager(BaseUserManager):
    '''
    Manager for users.
    '''
    def create_user(self, email, password=None, **extra_fields):
        '''
        Create and Save User
        '''
        if not email:
            raise ValueError('User must have an email. ')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        ''' Create and return a new superuser. '''
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    '''
    User Model
    '''

    email = models.EmailField(max_length=255, unique=True, verbose_name='信箱')
    name = models.CharField(max_length=255, verbose_name='暱稱')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self) -> str:
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    avatar = models.ImageField(null=True, blank=True,
                               upload_to=avatar_image_file_path,
                               verbose_name='頭貼')
    GENDER_CHOICES = (
        ('MALE', '男生'),
        ('FEMALE', '女生'),
        ('OTHER', '其他')
    )
    gender = models.CharField(max_length=6,
                              choices=GENDER_CHOICES,
                              default='OTHER',
                              verbose_name='性別')
    bio = RichTextField(null=True, blank=True, verbose_name='簡介')
    birthdate = models.DateField(null=True, blank=True, verbose_name='生日')
    country = CountryField(blank_label='(選擇國家/地區)', default='TW',
                           verbose_name='國家/地區')
    guitar_brand = models.CharField(max_length=20, null=True,
                                    blank=True, verbose_name='吉他品牌')
    guitar_model = models.CharField(max_length=20, null=True,
                                    blank=True, verbose_name='吉他型號')

    def __str__(self) -> str:
        return self.user.name

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
