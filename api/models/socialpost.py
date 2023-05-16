from django.db import models
from django.utils import timezone


class SocialPost(models.Model):
    """
    A schema for a social post.
    This schema defines the properties of a social post.
    """
    post = models.CharField(max_length=500)
    image = models.CharField(max_length=300, blank=True)
    likes = models.IntegerField(default=0)
    status = models.CharField(max_length=150, default="active")
    created_by = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)
