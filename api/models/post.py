from django.db import models
from django.utils import timezone


class Post(models.Model):
    """
    A schema for an article post.
    This schema defines the properties of an article.
    """
    title = models.CharField(max_length=300, blank=True)
    excerpt = models.CharField(max_length=500, blank=True)
    content = models.CharField(max_length=100000, blank=True)
    published = models.DateTimeField(default=timezone.now)
    category = models.CharField(max_length=150)
    image = models.CharField(max_length=300, blank=True)
    project_status = models.CharField(max_length=300, blank=True)
    event_date = models.DateTimeField(default=timezone.now)
    venue = models.CharField(max_length=300, blank=True)
    venue_link = models.CharField(max_length=300, blank=True)
    attendees = models.JSONField(default=dict)
    files = models.JSONField(default=dict)
    folder = models.CharField(max_length=300, blank=True)
    access = models.CharField(max_length=150, default="public")
    views = models.IntegerField(default=0)
    status = models.CharField(max_length=150, default="draft")
    step = models.CharField(max_length=150, default="writing")
    created_by = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)
