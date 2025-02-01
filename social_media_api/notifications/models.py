
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


User = settings.AUTH_USER_MODEL

'''notification model with user as actor and generic target which can b a post, comment, like'''


class Notification(models.Model):
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='actions')
    verb = models.CharField(max_length=255)
    # target_content_type = models.ForeignKey(
    #    ContentType, on_delete=models.CASCADE, null=True, blank=True)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('content_type', 'object_id')

    timestamp = models.DateTimeField(auto_now_add=True)

    def get_model_type(self):
        return self.__class__.__name__


#
#
#
#
#
#
