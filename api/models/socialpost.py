from django.db import models
from django.utils import timezone
from api.models.member import Member


class SocialPost(models.Model):
    """
    A schema for a social post.
    This schema defines the properties of a social post.
    """

    post = models.CharField(max_length=500)
    image = models.CharField(max_length=300, blank=True)
    likes = models.IntegerField(default=0)
    status = models.CharField(max_length=150, default="inactive")
    company = models.CharField(max_length=150, blank=True)
    author = models.CharField(max_length=150, blank=True)
    logo = models.CharField(max_length=150, blank=True)
    created_by = models.ForeignKey(
        Member,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=1,
        related_name="%(class)s_created",
    )
    created_at = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)
