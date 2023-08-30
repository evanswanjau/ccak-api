from django.db import models
from django.utils import timezone


class Donation(models.Model):
    """
    A schema for a donation.
    This schema defines the properties of an individual donation.
    """

    first_name = models.CharField(max_length=300)
    last_name = models.CharField(max_length=300)
    email = models.EmailField()
    phone_number = models.CharField(max_length=300)
    company = models.CharField(max_length=300, blank=True)
    designation = models.CharField(max_length=300, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    invoice_number = models.CharField(max_length=300, blank=True)
    status = models.CharField(max_length=150, default="unpaid")
    created_at = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)
