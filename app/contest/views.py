from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.models import Exists, OuterRef
from rest_framework import authentication, generics, mixins, permissions
from rest_framework.response import Response

from contest.serializers import (
    ContestCommentSerializer,
    ContestDetailSerializer,
    ContestSerializer,
)
from core.models import Comments, Contest, Likes
from core.permissions import IsOwnerOrReadOnly


class ContestView(generics.ListAPIView):

    queryset = Contest.objects.all()
    serializer_class = ContestSerializer
    search_fields = ["name"]
    ordering = ["pk"]


class ContestDetailView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Contest.objects.all()
    serializer_class = ContestDetailSerializer

    def get(self, request, *args, **kwargs):
        with transaction.atomic():
            contest = self.get_queryset().select_for_update().get(pk=kwargs["pk"])
            contest.views += 1
            contest.save()
        return self.retrieve(request, *args, **kwargs)

    def get_queryset(self):

        return Contest.objects.annotate(
            is_liked=Exists(
                Likes.objects.filter(user=self.request.user, object_id=OuterRef("pk"))
            )
        ).order_by("id")


class ContestLikeView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Contest.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset
        return queryset.filter(id=self.kwargs["pk"])

    def post(self, request, *args, **kwargs):
        contest = self.get_object()
        user = self.request.user
        is_like_obj = contest.likes.filter(user=user)
        if is_like_obj.exists():
            is_like_obj.delete()
            message = "dislike"
        else:
            contest.likes.create(user=user)
            message = "like"
        contest.save()

        return Response({"message": message})


class ContestCommentListView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Comments.objects.all()
    serializer_class = ContestCommentSerializer

    def get_queryset(self):
        queryset = self.queryset
        return queryset.filter(object_id=self.kwargs["pk"]).order_by("created_at")

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ContestCommentView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Comments.objects.all()
    serializer_class = ContestCommentSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    def get_contest(self):
        return Contest.objects.get(id=self.kwargs["pk"])

    def get_queryset(self):
        queryset = self.queryset
        return queryset.filter(object_id=self.kwargs["pk"]).order_by("created_at")

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        contest = self.get_contest()
        user = self.request.user
        content = self.request.data.get("content", None)
        contest_type = ContentType.objects.get_for_model(contest)
        if content is not None:
            comment = Comments.objects.create(
                user=user,
                content=content,
                object_id=self.kwargs["pk"],
                content_type_id=contest_type.id,
            )

            return Response({"data": ContestCommentSerializer(comment).data})


class ContestCommentActionView(
    mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView
):
    queryset = Comments.objects.all()
    serializer_class = ContestCommentSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
