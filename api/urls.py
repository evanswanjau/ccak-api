"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from api.views import posts
from api.views import members
from api.views import socialposts
from api.views import imagekit

urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts', posts.posts),
    path('post', posts.post),
    path('post/<int:post_id>', posts.post),
    path('members', members.members),
    path('member', members.member),
    path('member/<int:member_id>', members.member),
    path('socialposts', socialposts.socialposts),
    path('mysocialposts', socialposts.socialpost),
    path('socialpost', socialposts.socialpost),
    path('socialpost/<int:social_post_id>', socialposts.socialpost),
    path('imagekit/auth', imagekit.auth)
]
