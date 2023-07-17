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
from api.views import emails
from api.views import search
from api.views import auth
from api.views.members import MemberView
from api.views.posts import PostView
from api.views.subscriber import SubscriberView
from api.views.invoices import InvoiceView
from api.views.payments import PaymentView
from api.views.administrators import AdministratorView
from api.views import kopokopo

urlpatterns = [
    path('admin/', admin.site.urls),
    path('socialposts', socialposts.socialposts),
    path('mysocialposts', socialposts.socialpost),
    path('socialpost', socialposts.socialpost),
    path('socialpost/<int:social_post_id>', socialposts.socialpost),
    path('imagekit/auth', imagekit.auth),
    path('imagekit/upload', imagekit.upload_file),
    path('imagekit/delete', imagekit.delete_file),
    path('send/email', emails.send_custom_mail),
    path('member', MemberView.as_view(), name='create-member'),
    path('members', MemberView.as_view(), name='get-all-members'),
    path('member/<int:member_id>', MemberView.as_view(), name='get-member'),
    path('auth/member/login', auth.member_login),
    path('auth/administrator/login', auth.administrator_login),
    path('post', PostView.as_view(), name='create-post'),
    path('posts', PostView.as_view(), name='get-all-posts'),
    path('post/<int:post_id>', PostView.as_view(), name='get-post'),
    path('subscriber', SubscriberView.as_view(), name='create-subscriber'),
    path('subscribers', SubscriberView.as_view(), name='get-all-subscribers'),
    path('subscriber/<int:subscriber_id>', SubscriberView.as_view(), name='delete-subscriber'),
    path('search/posts', search.search_posts, name='search-posts'),
    path('search/members', search.search_members, name='search-members'),
    path('kopokopo/payment/receive', kopokopo.receive_payments),
    path('kopokopo/payment/process', kopokopo.process_payment),
    path('kopokopo/payment/query', kopokopo.query_payment),
    path('kopokopo/webhook/buygoods', kopokopo.buygoods_transaction_received_webhook),
    path('kopokopo/callback/buygoods', kopokopo.buygoods_transaction_received_callback),
    path('kopokopo/payments', kopokopo.get_all_kopokopo_payments),
    path('kopokopo/payment/<int:kopokopo_id>', kopokopo.get_single_kopokopo_payment),
    path('invoice', InvoiceView.as_view(), name='create-invoice'),
    path('invoices', InvoiceView.as_view(), name='get-all-invoices'),
    path('invoice/<int:invoice_id>', InvoiceView.as_view(), name='get-invoice'),
    path('payment', PaymentView.as_view(), name='create-payment'),
    path('payments', PaymentView.as_view(), name='get-all-payments'),
    path('payment/<int:payment_id>', PaymentView.as_view(), name='get-payment'),
    path('administrator', AdministratorView.as_view(), name='create-administrator'),
    path('administrators', AdministratorView.as_view(), name='get-all-administrators'),
    path('administrator/<int:administrator_id>', AdministratorView.as_view(), name='get-administrator'),
]
