# Generated by Django 5.1.4 on 2025-01-01 10:55

import taggit.managers
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_post_likes'),
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]