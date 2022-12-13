"""
Database models.
"""


import os
import uuid

from ckeditor.fields import RichTextField
from django import forms
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from taggit.managers import TaggableManager


def avatar_image_file_path(instance, filename):
    """Generate file path for new recipe image."""
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4()}{ext}"

    return os.path.join("uploads", "avatar", filename)


def artist_image_file_path(instance, filename):
    """Generate file path for artist images."""
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4()}{ext}"

    return os.path.join("uploads", "artist", filename)


class UserManager(BaseUserManager):
    """
    Manager for users.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and Save User
        """
        if not email:
            raise ValueError("User must have an email. ")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    User Model
    """

    email = models.EmailField(max_length=255, unique=True, verbose_name="信箱")
    name = models.CharField(max_length=255, verbose_name="暱稱")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # liked_contest = models.ManyToManyField('Contest', through='ContestLikes')

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["-id"]
        verbose_name = "用戶"
        verbose_name_plural = verbose_name
        get_latest_by = "id"


class Profile(models.Model):
    """Profile Model"""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    avatar = models.ImageField(
        null=True, blank=True, upload_to=avatar_image_file_path, verbose_name="頭貼"
    )
    GENDER_CHOICES = (("MALE", _("男生")), ("FEMALE", _("女生")), ("OTHER", _("其他")))
    gender = models.CharField(
        max_length=6, choices=GENDER_CHOICES, default="OTHER", verbose_name="性別"
    )
    bio = RichTextField(null=True, blank=True, verbose_name="簡介")
    birthdate = models.DateField(null=True, blank=True, verbose_name="生日")
    country = CountryField(blank_label="(選擇國家/地區)", default="TW", verbose_name="國家/地區")
    guitar_brand = models.CharField(
        max_length=20, null=True, blank=True, verbose_name="吉他品牌"
    )
    guitar_model = models.CharField(
        max_length=20, null=True, blank=True, verbose_name="吉他型號"
    )

    def __str__(self) -> str:
        return self.user.name

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class ChoiceArrayField(ArrayField):
    """
    A field that allows us to store an array of choices.

    Uses Django 1.9's postgres ArrayField
    and a MultipleChoiceField for its formfield.

    Usage:

    choices = ChoiceArrayField(models.CharField(max_length=...,
                               choices=(...,)), default=[...])
    """

    def formfield(self, **kwargs):
        defaults = {
            "form_class": forms.MultipleChoiceField,
            "choices": self.base_field.choices,
        }
        defaults.update(kwargs)
        return super(ArrayField, self).formfield(**defaults)


class Contest(models.Model):

    name = models.CharField(max_length=255, null=True, blank=False, verbose_name="比賽名稱")
    # 2022-10-18 request-contest-detail-fields -> remove date
    organizer = models.CharField(
        max_length=255, null=True, blank=False, verbose_name="主辦單位"
    )
    link = models.CharField(max_length=255, null=True, blank=True, verbose_name="連結")
    image = models.ImageField(max_length=255, null=True, blank=True, verbose_name="圖片")
    # 2022-10-29 edit-contest-model
    TYPE_CHOICES = (
        ("junior", _("高中組")),
        ("personal", _("個人組")),
        ("team", _("團體組")),
        ("fingerstyle", _("演奏組")),
        ("society", _("社會組")),
    )
    tags = TaggableManager(blank=True)
    # 2022-10-18 request-contest-detail-fields
    start_from = models.DateField(null=True, blank=True, verbose_name="開始於")
    end_at = models.DateField(null=True, blank=True, verbose_name="結束於")
    is_active = models.BooleanField(default=True)
    cover_image = models.ImageField(
        max_length=255, null=True, blank=True, verbose_name="封面圖片"
    )
    email = models.EmailField(max_length=255, verbose_name="聯絡信箱", blank=True)
    identity_restrictions = ChoiceArrayField(
        models.CharField(max_length=12, choices=TYPE_CHOICES, default="personal"),
        verbose_name="身份限制",
        blank=True,
        null=True,
    )
    regional_restrictions = CountryField(
        blank_label="(選擇國家/地區)", default="TW", verbose_name="國家/地區限制", blank=True
    )
    views = models.PositiveIntegerField(default=0, editable=False)
    likes = GenericRelation("Likes", related_query_name="contest")
    comments = GenericRelation("Comments")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="建立時間", editable=False
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="更新時間", editable=False
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["id"]
        verbose_name = "比賽"
        verbose_name_plural = verbose_name
        get_latest_by = "id"


class Likes(models.Model):
    """Define Like model."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)


class Comments(models.Model):
    """Define Comment model."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    content = RichTextField(null=False, blank=False, verbose_name="留言內容")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="建立時間", editable=False
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="更新時間", editable=False
    )

    class Meta:
        ordering = ["created_at"]
        verbose_name = "留言"
        verbose_name_plural = verbose_name
        get_latest_by = "created_at"


class Artist(models.Model):
    """Artist Model."""

    name = models.CharField(max_length=30, verbose_name="名字")
    avatar = models.ImageField(
        null=True, blank=True, upload_to=artist_image_file_path, verbose_name="頭貼"
    )
    cover = models.ImageField(
        null=True, blank=True, upload_to=artist_image_file_path, verbose_name="封面照片"
    )
    country = CountryField(blank_label="(選擇國家/地區)", default="TW", verbose_name="國家/地區")
    information = RichTextField(null=True, blank=True, verbose_name="簡介")
    website = models.URLField(max_length=200, blank=True, verbose_name="個人網站")
    fb_link = models.URLField(max_length=200, blank=True, verbose_name="Facebook")
    ig_link = models.URLField(max_length=200, blank=True, verbose_name="Instagram")
    yt_link = models.URLField(max_length=200, blank=True, verbose_name="Youtube")

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["id"]
        verbose_name = "指彈家"
        verbose_name_plural = verbose_name
        get_latest_by = "id"
