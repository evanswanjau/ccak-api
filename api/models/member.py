import datetime

from django.db import models
from django.utils import timezone


class Member(models.Model):
    """
    A schema for a member.
    This schema defines the properties of an individual member.
    """
    first_name = models.CharField(max_length=300)
    last_name = models.CharField(max_length=300)
    email = models.EmailField()
    phone_number = models.CharField(max_length=300)
    company = models.CharField(max_length=300)
    designation = models.CharField(max_length=300)
    password = models.CharField(max_length=300)
    bio = models.CharField(max_length=500, blank=True)
    technology = models.CharField(max_length=300, blank=True)
    company_email = models.CharField(max_length=300, blank=True)
    company_phone = models.CharField(max_length=300, blank=True)
    location = models.CharField(max_length=300, blank=True)
    website_link = models.CharField(max_length=300, blank=True)
    logo = models.CharField(max_length=300, blank=True)
    registration_status = models.CharField(max_length=150, default="unregistered")
    subscription_status = models.CharField(max_length=150, default="inactive")
    subscription_category = models.CharField(max_length=300, blank=True)
    subscription_expiry = models.DateField(default=datetime.date.today)
    status = models.CharField(max_length=150, default="active")
    step = models.CharField(max_length=150, blank=True)
    created_by = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)