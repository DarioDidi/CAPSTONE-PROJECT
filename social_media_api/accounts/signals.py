
from django.dispatch import receiver
from django.db.models.signals import post_save

from accounts.models import CustomUser
from posts.models import Post, Like, Comment, Repost
'''signal on creation of a like creates a notification'''


@receiver(post_save, sender=Like)
def like_notification(sender, instance, created, **kwargs):
    if created:
        # Assuming the post model has a user field for the author
        post = instance.post
        actor = instance.user
        recipient = post.author
        Notification.objects.create(
            recipient=recipient, actor=actor,  target=post, verb='liked your post')


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


# def markdown_find_mentions(markdown_text):
#    """
#    To find the users that mentioned
#    on markdown content using `BeautifulShoup`.
#
#    input  : `markdown_text` or markdown content.
#    return : `list` of usernames.
#    """
#    mark = markdownify(markdown_text)
#    soup = BeautifulSoup(mark, 'html.parser')
#    return list(set(
#        username.text[1::] for username in
#        soup.findAll('a', {'class': 'direct-mention-link'})
#    ))
#

def find_mentions(text):
    print("\n in find mentions \n")
    # TODO:check for @mentions not separated by spaces
    return [word[1:] for word in text.split() if word[0] == '@']


'''notify users tagged with @ in  post'''


@receiver(post_save, sender=Post)
def user_mention_notification(sender, instance, created, **kwargs):
    # if created:
    users = find_mentions(instance.content)
    for user in users:
        user_instance = CustomUser.objects.filter(username=user)
        if not user_instance.exists():
            continue
        post = instance
        actor = instance.author
        recipient = user_instance[0]
        print("recipient:", recipient)
        Notification.objects.get_or_create(
            recipient=recipient, actor=actor,  target=post, verb="tagged you in their post")
