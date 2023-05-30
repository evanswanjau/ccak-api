from django.db import models
from django.utils import timezone


class Search(models.Model):
    """
    A schema for a search query.
    This schema defines the properties of a search.
    """
    keyword = models.CharField(max_length=300, blank=True)
    table = models.CharField(max_length=300, blank=True)
    category = models.CharField(max_length=150, blank=True)
    project_status = models.CharField(max_length=150, blank=True)
    page = models.IntegerField(default=0)
    limit = models.IntegerField(default=0)
    ip_address = models.CharField(max_length=150, blank=True)
    created_by = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
