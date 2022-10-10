'''
Serializer for artist APIs.
'''
from core.models import Artist
from rest_framework import serializers

class ArtistSerializer(serializers.ModelSerializer):
    ''' Serializer for artist object. '''
    class Meta:
        model = Artist
        fields = '__all__'
        read_only_fields = ['id']