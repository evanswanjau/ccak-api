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
from api.views import imagekit
from api.views import emails
from api.views import auth
from api.views import posts
from api.views import socialposts
from api.views import comments
from api.views import members
from api.views import invoices
from api.views import payments
from api.views import donations
from api.views import subscribers
from api.views import administrators
from api.views import kopokopo
from api.views import home
from api.views import dashboard

from rest_framework_simplejwt.views import TokenObtainPairView

# fmt: off
urlpatterns = [
    path('', home.home),
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('imagekit/auth', imagekit.auth),
    path('imagekit/upload', imagekit.upload_file),
    path('imagekit/delete', imagekit.delete_file),
    path('send/email', emails.send_custom_mail),
    path('auth/member/login', auth.member_login),
    path('auth/administrator/login', auth.administrator_login),
    path('auth/resetlink', auth.reset_link),
    path('post/<int:post_id>', posts.get_post, name='get-post'),
    path('post', posts.create_post, name='create-post'),
    path('post/update/<int:post_id>', posts.update_post, name='update-post'),
    path('post/delete/<int:post_id>', posts.delete_post, name='delete-post'),
    path('posts/search', posts.search_posts, name='search-posts'),
    path('socialpost/<int:socialpost_id>', socialposts.get_socialpost, name='get-socialpost'),
    path('socialposts', socialposts.get_socialposts, name='get-socialposts'),
    path('socialpost', socialposts.create_socialpost, name='create-socialpost'),
    path('socialpost/update/<int:socialpost_id>', socialposts.update_socialpost, name='update-socialpost'),
    path('socialpost/delete/<int:socialpost_id>', socialposts.delete_socialpost, name='delete-socialpost'),
    path('socialposts/member/<int:member_id>', socialposts.member_socialposts, name='member-socialposts'),
    path('comment', comments.create_comment, name='create-comment'),
    path('comment/update/<int:comment_id>', comments.update_comment, name='update-comment'),
    path('comment/delete/<int:comment_id>', comments.delete_comment, name='delete-comment'),
    path('comments/socialpost/<int:socialpost_id>', comments.socialpost_comments, name='socialpost-comments'),
    path('member/<int:member_id>', members.get_member, name='get-member'),
    path('member', members.create_member, name='create-member'),
    path('member/update/<int:member_id>', members.update_member, name='update-member'),
    path('member/delete/<int:member_id>', members.delete_member, name='delete-member'),
    path('members/search', members.search_members, name='search-member'),
    path('kopokopo/payment/receive', kopokopo.receive_payments),
    path('kopokopo/payment/process', kopokopo.process_payment),
    path('kopokopo/payment/query', kopokopo.query_payment),
    path('kopokopo/webhook/buygoods', kopokopo.buygoods_transaction_received_webhook),
    path('kopokopo/callback/buygoods', kopokopo.buygoods_transaction_received_callback),
    path('kopokopo/payments', kopokopo.get_all_kopokopo_payments),
    path('kopokopo/payment/<int:kopokopo_id>', kopokopo.get_single_kopokopo_payment),
    path('invoice/<int:invoice_id>', invoices.get_invoice, name='get-invoice'),
    path('invoice', invoices.create_invoice, name='create-invoice'),
    path('invoice/update/<int:invoice_id>', invoices.update_invoice, name='update-invoice'),
    path('invoice/delete/<int:invoice_id>', invoices.delete_invoice, name='delete-invoice'),
    path('invoices/search', invoices.search_invoices, name='search-invoices'),
    path('payment/<int:payment_id>', payments.get_payment, name='get-payment'),
    path('payment', payments.create_payment, name='create-payment'),
    path('payment/update/<int:payment_id>', payments.update_payment, name='update-payment'),
    path('payment/delete/<int:payment_id>', payments.delete_payment, name='delete-payment'),
    path('payments/search', payments.search_payments, name='search-payments'),
    path('payments/mpesa/activate', payments.activate_mpesa_payment, name='activate-mpesa-payment'),
    path('donation/<int:donation_id>', donations.get_donation, name='get-donation'),
    path('donation', donations.create_donation, name='create-donation'),
    path('donation/update/<int:donation_id>', donations.update_donation, name='update-donation'),
    path('donation/delete/<int:donation_id>', donations.delete_donation, name='delete-donation'),
    path('donations/search', donations.search_donations, name='search-donations'),
    path('subscribers', subscribers.get_subscribers, name='get-subscribers'),
    path('subscriber', subscribers.create_subscriber, name='create-subscriber'),
    path('subscriber/delete/<int:subscriber_id>', subscribers.delete_subscriber, name='delete-subscriber'),
    path('administrators', administrators.get_administrators, name='get-administrators'),
    path('administrator', administrators.create_administrator, name='create-administrator'),
    path('administrator/<int:administrator_id>', administrators.get_administrator, name='get-administrator'),
    path('administrator/update/<int:administrator_id>', administrators.update_administrator, name='update-administrator'),
    path('administrator/delete/<int:administrator_id>', administrators.delete_administrator, name='delete-administrator'),
    path('dashboard/stats/general', dashboard.general_stats, name='get-general-status'),
    path('dashboard/stats/money', dashboard.money_stats, name='get-money-status'),
    path('dashboard/stats/member/', dashboard.member_stats, name='get-member-status'),

]
