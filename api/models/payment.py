from django.db import models
from django.utils import timezone


class Payment(models.Model):
    """
    A schema for a payment query.
    This schema defines the properties of a payment.
    """
    transaction_id = models.CharField(max_length=150, blank=True)
    method = models.CharField(max_length=150)
    invoice_number = models.CharField(max_length=150)
    timestamp = models.CharField(max_length=150)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_by = models.JSONField(default=dict)
    created_by = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)
