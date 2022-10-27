from contest.serializers import (ContestSerializer,
                                 ContestDetailSerializer,
                                 ContestLikeSerializer
                                 )
from rest_framework import generics, mixins, views
from core.models import Contest, ContestLikes
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import Http404
from rest_framework.permissions import IsAdminUser

class ContestView(generics.ListAPIView):

    queryset = Contest.objects.all()
    serializer_class = ContestSerializer
    search_fields = ['name']
    ordering = ['pk']


class ContestDetailView(mixins.RetrieveModelMixin,
                        generics.GenericAPIView):
    queryset = Contest.objects.all()
    serializer_class = ContestDetailSerializer

    def get_permission_classes(self):
        ''' Return the serializer class for requests. '''
        if self.action != 'get':
            return [IsAdminUser]

        return self.permission_classes

    def get(self, request, *args, **kwargs):
        contest = self.get_object()
        contest.views += 1
        contest.save()
        return self.retrieve(request, *args, **kwargs)


class ContestLikeView(mixins.CreateModelMixin,  generics.GenericAPIView):
    queryset = Contest.objects.all()
    serializer_class = ContestLikeSerializer

    def post(self, request, *args, **kwargs):
        contest = self.get_object()
        user = self.request.user
        if user in contest.likes.all():
            contest.likes.remove(user.id)
        else:
            contest.likes.add(user.id)
        contest.save()
        serializer = ContestLikeSerializer(contest)
        return Response(serializer.data)
