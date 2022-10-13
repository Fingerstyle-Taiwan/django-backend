from contest.serializers import ContestSerializer
from rest_framework import generics
from core.models import Contest


class ContestView(generics.ListAPIView):

    queryset = Contest.objects.all()
    serializer_class = ContestSerializer
    search_fields = ['name']
    ordering = ['pk']
