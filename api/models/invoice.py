from django.db import models
from django.utils import timezone


class Invoice(models.Model):
    """
    A schema for an invoice query.
    This schema defines the properties of an invoice.
    """
    invoice_number = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    items = models.JSONField(default=dict)
    status = models.CharField(max_length=150, default="unpaid")
    member_id = models.IntegerField(default=0)
    customer = models.JSONField(default=dict)
    created_by = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)
