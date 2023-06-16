from django.db import models
from django.utils import timezone


class Kopokopo(models.Model):
    """
    A schema for a kopokopo query.
    This schema defines the properties of a kopokopo.
    """
    topic = models.CharField(max_length=150)
    transaction_id = models.CharField(max_length=150)
    timestamp = models.CharField(max_length=150)
    event = models.JSONField(default=dict)
    links = models.JSONField(default=dict)
    created_at = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)
