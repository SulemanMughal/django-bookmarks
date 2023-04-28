from django.urls import path
from django.conf.urls import url
from django.contrib.auth.views import LoginView 
from .views import *
from django.views.generic import TemplateView
from bookmarks.feeds import *
from django.urls import path

urlpatterns = [

     path('latest/feed/', RecentBookmarks()),

    # Browsing
    url(r'^$', main_page, name="main_page"),
    url(r'^user/(\w+)/$', user_page, name="users_page"),
    url(r'^popular/$', popular_page, name="popular_page"),
    # Session management
    url(r'^login/$',  LoginView.as_view(), name="login_page" ),
    url(r'^logout/$', logout_page, name="logout_page"),
    url(r'^register/$', register_page, name="register_page"),
    url(r'^register/success/$', TemplateView.as_view( template_name =  'registration/register_success.html' ), name="registration_success"),
    # Account management
    url(r'^save/$', bookmark_save_page, name="bookmark_save"),
    url(r'^tag/([^\s]+)/$', tag_page, name="tag_page"),
    url(r'^tag/$', tag_cloud_page, name="tag_cloud_page"),
    url(r'^search/$', search_page, name="search_page"),

    # Ajax
    url(r'^ajax/tag/autocomplete/$', ajax_tag_autocomplete, name="ajax_tag_autocomplete_page"),

    url(r'^vote/$', bookmark_vote_page, name="bookmark_vote_page"),
    url(r'^bookmark/(\d+)/$', bookmark_page, name="bookmark_page"),


    # Friends
    url(r'^friends/(\w+)/$', friends_page, name="friends_page"),

    url(r'^friend/add/$', friend_add, name="friend_add"),
    url(r'^friend/invite/$', friend_invite, name="friend_invite_page"),
    url(r'^friend/accept/(\w+)/$', friend_accept),
]