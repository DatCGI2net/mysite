from __future__ import unicode_literals
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.safestring import SafeUnicode
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.CharField(max_length=255)
    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.TextField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        
        return "{0}category/{1}/".format(settings.SUB_SITE,self.name)
    
    
class Tag(models.Model):
    name = models.TextField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    
    
    def get_absolute_url(self):
        return "{0}tag/{1}/".format(settings.SUB_SITE, self.name)     
    
    def __str__(self):
        
        return self.name
    
class Post(models.Model):
    poster = models.ForeignKey('Profile', on_delete = models.CASCADE,)
    title = models.CharField(max_length =100, null = False)
    text  = models.TextField()
    pub_date=models.DateTimeField('date publish')
    slug = models.SlugField(max_length=40, unique=True)
    isPage = models.BooleanField(default=False)
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag)
    
    
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    def __str__(self):
        return self.title
        
    def get_comments(self):
        ##comments=Comment.objects.filter(post_id=self.id)
        comments=Comment.objects.filter(post=self.id, status=Comment.APPROVED)
        return comments
        
    def get_absolute_url(self):
        return "/blog/%i/" % self.id 
        
    class Meta:
        ordering = ["-pub_date"]
        
    
class Comment(models.Model):
    APPROVED='approved'
    UNAPPROVED='unapproved'
    SPAMMED='spammed'
    DELETED='deleted'
    COMMENT_CHOICES =((APPROVED,'Approved'),(UNAPPROVED,'Unapproved'),(SPAMMED,'Spammed'), (DELETED,'Deleted'))
    commenter=models.ForeignKey('Profile', on_delete=models.CASCADE,)
    #post_id=models.ForeignKey('Post',on_delete=models.CASCADE,)
    post=models.ForeignKey('Post',on_delete=models.CASCADE,)
    comments=models.TextField('Comments', null = False)
    comment_date=models.DateTimeField('date comment')
    status=models.CharField(max_length=10, choices=COMMENT_CHOICES,default=UNAPPROVED)
    
    def get_recent_comments(self):
        return self.comment_date <= timezone.now() - datetime.timedelta(days=5)
        
    def __str__(self):
        return SafeUnicode(self.comments)[:20]
        
    
    

    
