from contest.serializers import (
    ContestSerializer,
    ContestDetailSerializer,
    ContestCommentSerializer
)
from rest_framework import (
    generics,
    mixins,
    authentication,
    permissions,
    status
)
from core.models import Contest, Likes, Comments
from rest_framework.response import Response
from django.db.models import Exists, OuterRef


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


class ContestCommentView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Contest.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ContestCommentSerializer

    def get_queryset(self):
        queryset = self.queryset
        return queryset.filter(id=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        contest = self.get_object()
        user = self.request.user
        content = request.data.get('content', None)

        if content is not None:
            contest.comments.create(
                user=user,
                content=content
            )

            return Response({'status': 'success'})
        else:
            return Response({
                'status': 'error',
                'message': 'comment content cannot be null'
            }, status=status.HTTP_400_BAD_REQUEST)


class ContestCommentActionView(mixins.CreateModelMixin,
                               generics.GenericAPIView):
    queryset = Comments.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ContestCommentSerializer

    def get_queryset(self):
        return self.queryset.filter(id=self.kwargs['pk'])

    def patch(self, request, *args, **kwargs):
        user = self.request.user
        content = request.data.get('content', None)
        comment = self.get_object()

        if comment.user == user:
            comment.content = content
            comment.save()

            return Response({'status': 'success'})
        else:
            return Response({
                'status': 'error',
                'message': 'comment user mismatch'
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        comment = self.get_object()

        if comment.user == user:
            comment.delete()

            return Response({'status': 'success'})
        else:
            return Response({
                'status': 'error',
                'message': 'comment user mismatch'
            }, status=status.HTTP_400_BAD_REQUEST)
