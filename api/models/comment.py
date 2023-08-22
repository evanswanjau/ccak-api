from django.db import models
from django.utils import timezone
from api.models.member import Member
from api.models.socialpost import SocialPost
from api.models.invoice import Invoice


class Comment(models.Model):
    """
    A schema for comments on social posts.
    """

    comment = models.CharField(max_length=500)
    socialpost = models.IntegerField(default=0)
    status = models.CharField(max_length=150, default="active")
    company = models.CharField(max_length=150, blank=True)
    author = models.CharField(max_length=150, blank=True)
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
