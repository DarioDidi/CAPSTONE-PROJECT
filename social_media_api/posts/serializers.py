from rest_framework import serializers

from .models import Post, Comment, Like, Repost
from accounts.serializers import CustomUserSerializer, BaseUserSmallSerializer  # type: ignore
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)

''' use methods for likes and taggit's serializer for tags'''


class PostSerializer(serializers.ModelSerializer):
    author = BaseUserSmallSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    reposts = serializers.SerializerMethodField()
    tags = TagListSerializerField()

    class Meta:
        model = Post
        fields = '__all__'
        extra_fields = ['likes_count']

        read_only_fields = ['author']

    def get_likes_count(self, obj):
        return obj.likes.count()

    ''' return only user id for post likes since we already know the post '''

    def get_likes(self, obj):
        return [post.id for post in obj.likes.all()]

    def get_reposts(self, obj):
        return obj.reposts.count()


'''serializer specifically for editing posts'''


class PostUpdateSerializer(serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Post
        # Only these fields can be updated
        fields = ['title', 'content', 'tags']
        extra_kwargs = {
            'id': {'read_only': True},
        }


class RepostSerializer(serializers.ModelSerializer):
    user = BaseUserSmallSerializer(read_only=True)
    original_post = PostSerializer()

    class Meta:
        model = Repost
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    # nested serializer for the related Post
    post = PostSerializer(read_only=True)
    author = CustomUserSerializer(read_only=True)
    likes = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'
        extra_fields = "like_count"

    def get_likes(self, obj):
        return [comment.id for comment in obj.likes.all()]

    def get_like_count(self, obj):
        return obj.likes.count()


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['created_at']

    '''add user and post to like before saving'''

    def create(self, validated_data):
        user = validated_data['user']
        post = validated_data['post']

        existing_instance = Like.objects.filter(post=post, user=user).first()
        # if post already liked
        if existing_instance:
            return existing_instance
        return super().create(validated_data)
