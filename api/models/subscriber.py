from django.db import models
from django.utils import timezone


class Subscriber(models.Model):
    """
        A schema for a subscriber.
        This schema defines the properties of a mail subscriber.
        """
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(default=timezone.now)
