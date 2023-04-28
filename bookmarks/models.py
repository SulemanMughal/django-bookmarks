from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from django.conf import settings


# Create your models here.


class Link(models.Model):
    url = models.URLField(unique=True)


    def __str__(self):
        return self.url

class Bookmark(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title of the Bookmark", blank=False, null=False, default="")
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    link = models.ForeignKey(Link, on_delete=models.CASCADE)


    def __str__(self):
        return self.title

    
    def get_absolute_url(self):
        return self.link.url



class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)
    bookmarks = models.ManyToManyField(Bookmark)


    def __str__(self):
        return self.name

class SharedBookmark(models.Model):
    bookmark = models.ForeignKey(Bookmark, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    votes = models.IntegerField(default=1)
    users_voted = models.ManyToManyField(get_user_model() )

    def __str__(self):
        return  self.bookmark.title


class Friendship(models.Model):
    from_friend = models.ForeignKey(
    get_user_model(), related_name='friend_set',
    on_delete=models.CASCADE
    )
    to_friend = models.ForeignKey(
    get_user_model(), related_name='to_friend_set',
    on_delete=models.CASCADE
    )


    def __str__(self):
        return '%s, %s' % (
        self.from_friend.username,
        self.to_friend.username
        )


    class Meta:
        unique_together = (('to_friend', 'from_friend'), )


class Invitation(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    code = models.CharField(max_length=20)
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    
    def __str__(self):
        return '%s, %s' % (self.sender.username, self.email)
    
    def send(self):
        subject = 'Invitation to join Django Bookmarks'
        link = '%s/friend/accept/%s/' % (
        settings.SITE_REDIRECT_ORIGINAL,
        self.code
        )
        template = get_template('Email/invitation_email.txt')
        context = {
        'name': self.name,
        'link': link,
        'sender': self.sender.username,
        }
        message = template.render(context)
        send_mail(
        subject, message,
        settings.DEFAULT_FROM_EMAIL, [self.email]
        )