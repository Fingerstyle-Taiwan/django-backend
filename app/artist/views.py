"""
Views for artist API.
"""
from rest_framework import mixins
from rest_framework.generics import GenericAPIView

from artist.serializer import ArtistSerializer
from core.models import Artist


class ListArtists(mixins.ListModelMixin, GenericAPIView):
    serializer_class = ArtistSerializer
    queryset = Artist.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
