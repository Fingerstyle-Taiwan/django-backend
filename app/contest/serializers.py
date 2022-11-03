from core.models import Contest, Comments
from rest_framework import serializers
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)


class ContestSerializer(TaggitSerializer, serializers.ModelSerializer):
    like_count = serializers.IntegerField(
        source='likes.count',
        read_only=True
    )
    comment_count = serializers.IntegerField(
        source='comments.count',
        read_only=True
    )
    tags = TagListSerializerField()

    class Meta:
        model = Contest
        fields = [
            'id',
            'name',
            'organizer',
            'like_count',
            'comment_count',
            'tags'
        ]


class ContestCommentSerializer(TaggitSerializer, serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name')

    class Meta:
        model = Comments
        fields = ['id', 'content', 'user_name', 'updated_at']


class ContestDetailSerializer(TaggitSerializer, serializers.ModelSerializer):
    like_count = serializers.IntegerField(
        source='likes.count',
        read_only=True
    )
    is_liked = serializers.BooleanField(read_only=True, default=False)
    comments = ContestCommentSerializer(many=True)
    tags = TagListSerializerField()

    class Meta:
        model = Contest
        fields = '__all__'
        extra_fields = ['like_count', 'is_liked', 'comments', 'tags']
