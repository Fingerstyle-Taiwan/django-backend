from contest.serializers import *
from rest_framework import generics

class ContestView(generics.ListAPIView):
    queryset = Contest.objects.all()
    serializer_class = ContestSerializer
    search_fields = ['name']
    ordering = ['pk']
    