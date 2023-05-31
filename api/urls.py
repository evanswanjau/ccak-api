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
from api.views import socialposts
from api.views import imagekit
from api.views import search
from api.views import auth
from api.views.members import MemberView
from api.views.posts import PostView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('search', search.search),
    path('socialposts', socialposts.socialposts),
    path('mysocialposts', socialposts.socialpost),
    path('socialpost', socialposts.socialpost),
    path('socialpost/<int:social_post_id>', socialposts.socialpost),
    path('imagekit/auth', imagekit.auth),
    path('member', MemberView.as_view(), name='create-member'),
    path('members', MemberView.as_view(), name='get-all-members'),
    path('member/<int:member_id>', MemberView.as_view(), name='get-member'),
    path('auth/member/login', auth.member_login),
    path('post', PostView.as_view(), name='create-post'),
    path('posts', PostView.as_view(), name='get-all-posts'),
    path('post/<int:post_id>', PostView.as_view(), name='get-post'),
]
