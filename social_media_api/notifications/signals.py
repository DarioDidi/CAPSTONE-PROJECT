
from django.db.models.base import pre_save
from django.dispatch import receiver
from django.db.models.signals import post_save

from accounts.models import CustomUser
from posts.models import Post, Like, Comment, Repost
from .models import Notification

'''signal on creation of a like creates a notification'''


@receiver(post_save, sender=Like)
def like_notification(sender, instance, created, **kwargs):
    print("\n\n created a like!\n\n")
    if created:
        # Assuming the post model has a user field for the author
        post = instance.post
        if post:
            actor = instance.user
            recipient = post.author
            Notification.objects.create(
                recipient=recipient, actor=actor,  target=post, verb='liked your post')

        comment = instance.comment
        if comment:
            actor = instance.user
            recipient = comment.author
            Notification.objects.create(
                recipient=recipient, actor=actor,  target=comment, verb='liked your comment')


'''signal on creation of a comment creates a notification'''


@receiver(post_save, sender=Comment)
def comment_notification(sender, instance, created, **kwargs):
    if created:
        # Assuming the post model has a user field for the author
        post = instance.post
        actor = instance.author
        recipient = post.author
        Notification.objects.create(
            recipient=recipient, actor=actor,  target=post, verb="Commented on your post")


'''signal on creation of a repost creates a notification'''


@receiver(post_save, sender=Repost)
def repost_notification(sender, instance, created, **kwargs):
    if created:
        # Assuming the post model has a user field for the author
        post = instance.original_post
        actor = instance.user
        recipient = post.author
        Notification.objects.create(
            recipient=recipient, actor=actor,  target=post, verb="reposted your post")


def find_mentions(text):
    print("\n in find mentions \n")
    # TODO:check for @mentions not separated by spaces
    return [word for word in text.split() if word[0] == '@']


'''notify users tagged with @ in  post'''


@receiver(pre_save, sender=Post)
def save_old_content(sender, instance, **kwargs):
    if instance.pk:
        instance.old_content = instance.__class__.objects.get(
            pk=instance.pk).content


@receiver(post_save, sender=Post)
def user_mention_notification(sender, instance, created, **kwargs):
    users = find_mentions(instance.content)
    found = [user for user in users]
    if instance.old_content:
        for user in users:
            if user in instance.old_content:
                found.remove(user)

    users = [user[1:] for user in found]
    for user in users:
        user_instance = CustomUser.objects.filter(username=user)
        if not user_instance.exists():
            continue
        post = instance
        actor = instance.author
        recipient = user_instance[0]
        Notification.objects.create(
            recipient=recipient, actor=actor,  target=post, verb="tagged you in their post")
