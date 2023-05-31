from django.contrib import admin
from api.models.post import Post
from api.models.member import Member
from api.models.socialpost import SocialPost
from api.models.search import Search
from api.models.subscriber import Subscriber

admin.site.register(Post)
admin.site.register(Member)
admin.site.register(SocialPost)
admin.site.register(Search)
admin.site.register(Subscriber)
