import datetime

from django.db import models
from django.utils import timezone


class Administrator(models.Model):
    """
    A schema for an administrator.
    This schema defines the properties of an individual administrator.
    """
    first_name = models.CharField(max_length=300)
    last_name = models.CharField(max_length=300)
    email = models.EmailField()
    password = models.CharField(max_length=300)
    role = models.CharField(max_length=300, default="admin")
    status = models.CharField(max_length=150, default="active")
    created_by = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)
