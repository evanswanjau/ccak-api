from django.db import models
from django.utils import timezone
from api.models.administrator import Administrator


class Post(models.Model):
    """
    A schema for an article post.
    This schema defines the properties of an article.
    """

    title = models.CharField(max_length=300, blank=True)
    excerpt = models.CharField(max_length=500, blank=True)
    tags = models.JSONField(default=dict)
    content = models.TextField(blank=True)
    published = models.DateTimeField(default=timezone.now, db_index=True)
    category = models.CharField(max_length=150)
    image = models.CharField(max_length=300, blank=True)
    project_status = models.CharField(max_length=300, blank=True)
    event_date = models.DateTimeField(default=timezone.now, db_index=True)
    venue = models.CharField(max_length=300, blank=True)
    venue_link = models.CharField(max_length=300, blank=True)
    attendees = models.JSONField(default=dict)
    files = models.JSONField(default=dict)
    folder = models.CharField(max_length=300, blank=True)
    access = models.CharField(max_length=150, default="public")
    views = models.IntegerField(default=0)
    status = models.CharField(max_length=150, default="draft")
    step = models.CharField(max_length=150, default="writing")
    author = models.CharField(max_length=150, blank=True)
    created_by = models.ForeignKey(
        Administrator,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=1,
        related_name="%(class)s_created",  # Customize related name as needed
    )
    created_at = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)
