"""
Serializer for artist APIs.
"""
from rest_framework import serializers

from core.models import Artist


class ArtistSerializer(serializers.ModelSerializer):
    """Serializer for artist object."""

    class Meta:
        model = Artist
        fields = "__all__"
        read_only_fields = ["id"]
