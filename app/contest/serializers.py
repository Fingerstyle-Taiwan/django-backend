from dataclasses import fields
from core.models import Contest
from rest_framework import serializers


class ContestSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(
        source='likes.count',
        read_only=True
    )

    class Meta:
        model = Contest
        fields = ['id', 'name', 'organizer', 'like_count']


class ContestDetailSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(
        source='likes.count',
        read_only=True
    )

    class Meta:
        model = Contest
        exclude = ['likes']
        extra_fields = ['like_count']



class ContestLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contest
        fields = ['id', 'likes']
