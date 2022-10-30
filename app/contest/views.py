from contest.serializers import (ContestSerializer,
                                 ContestDetailSerializer,
                                 )
from rest_framework import generics, mixins, authentication, permissions
from core.models import Contest, Likes
from rest_framework.response import Response
from django.db.models import Exists, OuterRef
from django.contrib.contenttypes.models import ContentType

class ContestView(generics.ListAPIView):

    queryset = Contest.objects.all()
    serializer_class = ContestSerializer
    search_fields = ['name']
    ordering = ['pk']


class ContestDetailView(mixins.RetrieveModelMixin,
                        generics.GenericAPIView):
    queryset = Contest.objects.all()
    serializer_class = ContestDetailSerializer

    def get(self, request, *args, **kwargs):
        contest = self.get_object()
        contest.views += 1
        contest.save()
        return self.retrieve(request, *args, **kwargs)

    def get_queryset(self):

        return Contest.objects.annotate(is_liked=Exists(
               Likes.objects.filter(user=self.request.user,
                                           object_id=OuterRef('pk')))) \
                                           .order_by('id')


class ContestLikeView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Contest.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset
        return queryset.filter(id=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        contest = self.get_object()
        user = self.request.user
        is_like_obj = contest.likes.filter(user=user)
        if is_like_obj.exists():
            is_like_obj.delete()
            message = 'dislike'
        else:
            contest.likes.create(user=user)
            message = 'like'
        contest.save()

        return Response({'message': message})
