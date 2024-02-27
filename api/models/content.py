from django.db import models
from django.utils import timezone


class Content(models.Model):
    """
    A schema for content for all the pages
    """

    page = models.CharField(max_length=150)
    section = models.IntegerField(default=150)
    content = models.JSONField(default=dict)
    created_at = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)
