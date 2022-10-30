from core.models import Contest
from rest_framework import serializers
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)


class ContestSerializer(TaggitSerializer, serializers.ModelSerializer):
    like_count = serializers.IntegerField(
        source='likes.count',
        read_only=True
    )
    tags = TagListSerializerField()

    class Meta:
        model = Contest
        fields = ['id', 'name', 'organizer', 'like_count', 'tags']


class ContestDetailSerializer(TaggitSerializer, serializers.ModelSerializer):
    like_count = serializers.IntegerField(
        source='likes.count',
        read_only=True
    )
    is_liked = serializers.BooleanField(read_only=True, default=False)
    tags = TagListSerializerField()

    class Meta:
        model = Contest
        fields = '__all__'
        extra_fields = ['like_count', 'is_liked', 'tags']
