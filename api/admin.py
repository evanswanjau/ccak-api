from django.contrib import admin
from api.models.post import Post
from api.models.member import Member
from api.models.socialpost import SocialPost

admin.site.register(Post)
admin.site.register(Member)
admin.site.register(SocialPost)
