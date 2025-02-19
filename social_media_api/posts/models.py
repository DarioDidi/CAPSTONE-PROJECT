from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.conf import settings

from taggit.managers import TaggableManager

from accounts.models import CustomUser  # type: ignore

from notifications.models import Notification


class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    content = models.TextField(max_length=1000)
    old_content = models.TextField(max_length=1000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(
        CustomUser, related_name='post_likes', blank=True)
    tags = TaggableManager()
    reposts = models.ManyToManyField(
        'self', symmetrical=False, related_name='original_post')

    notifications = GenericRelation(
        Notification, related_query_name='post_notifications')

    class Meta:
        ordering = ['created_at']  # Order posts by creation date
        verbose_name = 'Social Media Post'
        verbose_name_plural = 'Social Media Posts'

    def get_model_type(self):
        return self.__class__.__name__


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(
        CustomUser, related_name='comment_likes', blank=True)

    class Meta:
        ordering = ['created_at']

    def get_model_type(self):
        return self.__class__.__name__


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    post = models.ForeignKey(
        'Post', on_delete=models.CASCADE, blank=True, null=True)
    comment = models.ForeignKey(
        'Comment', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    '''ensure a user can like a post only once'''
    class Meta:
        unique_together = (('post', 'user'), ('comment', 'user'),)

    def get_model_type(self):
        return self.__class__.__name__


class Repost(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    original_post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='repost')
    reposted_at = models.DateTimeField(auto_now_add=True)


#
