from re import template
import json
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from bookmarks.forms import *
from .models import *
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta
import pytz
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils.translation import gettext as _


# Main Page
def main_page(request):
    shared_bookmarks = SharedBookmark.objects.order_by(
    '-date'
    )[:10]
    template_name = "main_page.html"
    context = {
    'head_title': 'Django Bookmarks',
    'page_title': 'Welcome to Django Bookmarks',
    'page_body': 'Where you can store and share bookmarks!',
    'shared_bookmarks': shared_bookmarks
    }
    return render(request, template_name, context)


# User Detail Page

def user_page(request, username):
    template_name="user_page.html"
    user = get_object_or_404(User, username=username)
    query_set = user.bookmark_set.order_by('-id')
    ITEMS_PER_PAGE = settings.ITEMS_PER_PAGE
    paginator = Paginator(query_set, ITEMS_PER_PAGE)
    is_friend = Friendship.objects.filter(
    from_friend=request.user,
    to_friend=user
    )
    try:
            page = int(request.GET['page'])
    except:
        page = 1
    try:
        bookmarks = paginator.page(page)
    except:
        raise Http404
    context =  {
        'bookmarks': bookmarks,
        'username': username,
        'show_tags': True,
        'show_edit': username == request.user.username,
        'show_paginator': paginator.num_pages > 1,
        'has_prev': bookmarks.has_previous(),
        'has_next': bookmarks.has_next(),
        'page': bookmarks,
        'pages': paginator.num_pages,
        'next_page': page + 1,
        'prev_page': page - 1,
        'is_friend': is_friend
    }
    return render(request, template_name, context)

# Logout Page
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


# Registration Page
def register_page(request):
    template_name= "registration/register.html"
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            if 'invitation' in request.session:
                # Retrieve the invitation object.
                invitation = Invitation.objects.get(id=request.session['invitation'])
                # Create friendship from user to sender.
                friendship = Friendship(
                from_friend=user,
                to_friend=invitation.sender
                )
                friendship.save()
                # Create friendship from sender to user.
                friendship = Friendship (
                from_friend=invitation.sender,
                to_friend=user
                )
                friendship.save()
                # Delete the invitation from the database and session.
                invitation.delete()
                del request.session['invitation']
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
        context ={
            'form': form
        }
        return render(request, template_name, context)



def bookmark_save_page(request):
    ajax = request.GET.get('ajax', None)
    if request.method == 'POST':
        print(request.POST)
        form = BookmarkSaveForm(request.POST)
        if form.is_valid():
            bookmark = _bookmark_save(request, form)
            if ajax:
                context =  {
                'bookmarks': [bookmark],
                'show_edit': True,
                'show_tags': True
                }
                return render(request , 'bookmark_list.html', context)
            else:
                return HttpResponseRedirect(
                '/user/%s/' % request.user.username
                )
        else:
            if ajax:
                return HttpResponse('failure')
    elif  'url' in request.GET:
        url = request.GET['url']
        title = ''
        tags = ''
        try:
            link = Link.objects.get(url=url)
            bookmark = Bookmark.objects.get(link=link, user=request.user)
            title = bookmark.title
            tags = ' '.join(tag.name for tag in bookmark.tag_set.all())
        except:
            pass
        form = BookmarkSaveForm({
        'url': url,
        'title': title,
        'tags': tags
        })
    else:
        form = BookmarkSaveForm()
    context =  {
    'form': form
    }
    if ajax:
        return render(request,
        'bookmark_save_form.html',
        context
        )
    else:
        return render(request,
        'bookmark_save.html',
        context
        )



def tag_page(request, tag_name):
    template_name="tag_page.html"
    tag = get_object_or_404(Tag, name=tag_name)
    bookmarks = tag.bookmarks.order_by('-id')
    context =  {
        'bookmarks': bookmarks,
        'tag_name': tag_name,
        'show_tags': True,
        'show_user': True
    }
    return render(request, template_name, context)


def tag_cloud_page(request):
    template_name="tag_cloud_page.html"
    MAX_WEIGHT = settings.MAX_WEIGHT
    tags = Tag.objects.order_by('name')
    # Calculate tag, min and max counts.
    min_count = max_count = tags[0].bookmarks.count()
    for tag in tags:
        tag.count = tag.bookmarks.count()
        if tag.count < min_count:
            min_count = tag.count
        if max_count < tag.count:
            max_count = tag.count
    # Calculate count range. Avoid dividing by zero.
    range = float(max_count - min_count)
    if range == 0.0:
        range = 1.0
    # Calculate tag weights.
    for tag in tags:
        tag.weight = int(
            MAX_WEIGHT * (tag.count - min_count) / range
        )
    context =  {
        'tags': tags
    }
    return render(request, template_name, context)


def search_page(request):
    template_name="search.html"
    template_name_1="bookmark_list.html"
    form = SearchForm()
    bookmarks = []
    show_results = False
    if 'query' in request.GET:
        show_results = True
        query = request.GET['query'].strip()
        if query:
            keywords = query.split()
            q = Q()
            for keyword in keywords:
                q = q & Q(title__icontains=keyword)
            form = SearchForm({'query' : query})
            bookmarks = Bookmark.objects.filter(q)[:10]
    context =  { 
        'form': form,
        'bookmarks': bookmarks,
        'show_results': show_results,
        'show_tags': True,
        'show_user': True
    }
    if 'ajax' in  request.GET:
        return render(request, template_name_1, context)
    else:
        return render(request, template_name, context)
    
def _bookmark_save(request, form):
    # Create or get link.
    link, dummy =  Link.objects.get_or_create(url=form.cleaned_data['url'])
    # Create or get bookmark.
    bookmark, created = Bookmark.objects.get_or_create(
    user=request.user,
    link=link
    )
    # Update bookmark title.
    bookmark.title = form.cleaned_data['title']
    # If the bookmark is being updated, clear old tag list.
    if not created:
        bookmark.tag_set.clear()
    # Create new tag list.
    tag_names = form.cleaned_data['tags'].split()
    for tag_name in tag_names:
        tag, dummy = Tag.objects.get_or_create(name=tag_name)
        bookmark.tag_set.add(tag)
    # Share on the main page if requested.
    if form.clean_data['share']:
        shared_bookmark, created = SharedBookmark.objects.get_or_create(
        bookmark=bookmark
        )
        if created:
            shared_bookmark.users_voted.add(request.user)
            shared_bookmark.save()
    # Save bookmark to database and return it.
    bookmark.save()
    return bookmark


def ajax_tag_autocomplete(request):
    # if 'term' in  request.GET:
    #     tags = Tag.objects.filter(name__istartswith=request.GET['term'])[:]
    #     print(tags)
    #     return HttpResponse('\n'.join(tag.name for tag in tags))
    # return HttpResponse()
    if request.is_ajax():
        q = request.GET.get('term', '').capitalize()
        tags = Tag.objects.filter(name__istartswith=request.GET['term'])[:]
        results = []
        for tag in tags:
            results.append(tag.name)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


@login_required
def bookmark_vote_page(request):
    if 'id' in  request.GET:
        try:
            id = request.GET['id']
            shared_bookmark = SharedBookmark.objects.get(id=id)
            user_voted = shared_bookmark.users_voted.filter(
            username=request.user.username
            )
            if not user_voted:
                shared_bookmark.votes += 1
                shared_bookmark.users_voted.add(request.user)
                shared_bookmark.save()
        except ObjectDoesNotExist:
            raise Http404('Bookmark not found.')
    if 'HTTP_REFERER' in request.META:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    return HttpResponseRedirect('/')


def popular_page(request):
    template_name="popular_page.html"
    today = timezone.now()
    yesterday = today - timedelta(1)
    shared_bookmarks = SharedBookmark.objects.filter(
    date__gt=yesterday
    )
    shared_bookmarks = shared_bookmarks.order_by(
    '-votes'
    )[:10]
    context =  {
        'shared_bookmarks': shared_bookmarks
    }
    return render(request, template_name,  context)


def bookmark_page(request, bookmark_id):
    template_name="bookmark_page.html"
    shared_bookmark = get_object_or_404(
    SharedBookmark,id=bookmark_id
    )
    context =  {
        'shared_bookmark': shared_bookmark
    }
    return render(request ,template_name, context)


def friends_page(request, username):
    template_name="friends_page.html"
    user = get_object_or_404(User, username=username)
    friends = [friendship.to_friend for friendship in user.friend_set.all()]
    friend_bookmarks =  Bookmark.objects.filter(user__in=friends).order_by('-id')
    context ={
        'username': username,
        'friends': friends,
        'bookmarks': friend_bookmarks[:10],
        'show_tags': True,
        'show_user': True
    }
    return render(request, template_name, context)


@login_required
def friend_add(request):
    if 'username' in  request.GET:
        friend = get_object_or_404(User, username=request.GET['username'])
        friendship = Friendship(
        from_friend=request.user,
        to_friend=friend
        )
        try:
            friendship.save()
            messages.add_message(request, messages.INFO,'%s was added to your friend list.' % friend.username
            )
        except:
                messages.add_message(request, messages.INFO,'%s is already a friend of yours.' % friend.username
            )
        return HttpResponseRedirect(
        '/friends/%s/' % request.user.username
        )
    else:
        raise Http404


@login_required
def friend_invite(request):
    template_name="friend_invite.html"
    if request.method == 'POST':
        form = FriendInviteForm(request.POST)
        if form.is_valid():
            invitation = Invitation(
            name = form.cleaned_data['name'],
            email = form.cleaned_data['email'],
            code = User.objects.make_random_password(20),
            sender = request.user
            )
            invitation.save()
            try:
                invitation.send()
                messages.add_message(request, messages.INFO,_('An invitation was sent to %s.') % invitation.email
                )
            except:
                messages.add_message(request, messages.INFO, _('There was an error while sending the invitation.')
                )
            return HttpResponseRedirect('/friend/invite/')
    else:
        form = FriendInviteForm()
    context =  {
    'form': form
    }
    return render(request, template_name, context)


def friend_accept(request, code):
    invitation = get_object_or_404(Invitation, code__exact=code)
    request.session['invitation'] = invitation.id
    return HttpResponseRedirect('/register/')

