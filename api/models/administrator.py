from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class Administrator(AbstractUser):
    """
    A schema for an administrator.
    This schema defines the properties of an individual administrator.
    """

    # Your existing fields
    username = models.CharField(max_length=150, default="")
    role = models.CharField(max_length=300, default="admin")
    status = models.CharField(max_length=150, default="active")
    created_by = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)

    # Update related_name to avoid clashes with default user model
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='admin_users',
        related_query_name='admin_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='admin_users_permissions',
        related_query_name='admin_user_permission',
    )

    def save(self, *args, **kwargs):
        # Ensure username is set to email before saving
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)