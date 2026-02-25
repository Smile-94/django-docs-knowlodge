from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel, TimeStampedModel


# <<------------------------------------User Model Manager---------------------------------------->>
class UserManager(BaseUserManager):
    def create_superuser(self, username, email, password, **extra_fields):
        if not username or not email or not password:
            raise ValueError(_("You must provide valid username, email and password"))

        user = self.model(username=username, email=email, password=password, is_superuser=True, is_staff=True)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError(_("You must provide a username"))

        if not email:
            raise ValueError(_("You must provide a email"))

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.full_clean()
        user.save()
        return user


# <<------------------------------------User Model---------------------------------------->>ssss
class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    username = models.CharField(max_length=100, unique=True, null=True, blank=True, validators=[UnicodeUsernameValidator()])
    email = models.EmailField(_("email address"), unique=True, null=True, blank=True)
    phone = models.CharField(max_length=100, unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    class Meta:
        app_label = "user"
        db_table = "user"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def get_user_rbac_permissions(self):
        return self.role.permissions.all().prefetch_related("permissions")

    def get_short_name(self):
        return self.username

    def __str__(self):
        return f"{self.username}"

    def __repr__(self):
        return f"<User: {self.username}, {self.pk}>"


class UserSession(BaseModel, TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="device_sessions")
    device_id = models.CharField(max_length=255)
    session_key = models.CharField(max_length=255, unique=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    login_at = models.DateTimeField(default=timezone.now)
    last_activity = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "user_device_sessions"
        verbose_name = "User Session"
        verbose_name_plural = "User Sessions"

    def __str__(self):
        return f"{self.user.username} - {self.device_id} - {self.city}, {self.country}"


class UserDeviceToken(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="device_tokens")
    device_id = models.CharField(max_length=255)
    access_token_hash = models.CharField(max_length=255, unique=True, blank=True, null=True)
    refresh_token_hash = models.CharField(max_length=255, unique=True, blank=True, null=True)
    user_agent_hash = models.CharField(max_length=255, blank=True, null=True)
    browser_fingerprint = models.CharField(max_length=255, blank=True, null=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField()
    is_active = models.BooleanField(default=True)
    access_expires_at = models.DateTimeField(blank=True, null=True)
    refresh_expires_at = models.DateTimeField(blank=True, null=True)
    rotated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "user_device_tokens"
        verbose_name = "User Device Token"
        verbose_name_plural = "User Device Tokens"

    def __str__(self):
        return f"{self.user.username} - {self.device_id}"
