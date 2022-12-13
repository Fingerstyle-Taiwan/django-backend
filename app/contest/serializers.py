from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField

from core.models import Comments, Contest


class ContestSerializer(TaggitSerializer, serializers.ModelSerializer):
    like_count = serializers.IntegerField(source="likes.count", read_only=True)
    comment_count = serializers.IntegerField(source="comments.count", read_only=True)
    tags = TagListSerializerField()

    class Meta:
        model = Contest
        fields = ["id", "name", "organizer", "like_count", "comment_count", "tags"]


class ContestCommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.name", read_only=True)

    class Meta:
        model = Comments
        fields = ["id", "user_name", "content", "created_at", "updated_at"]
        ordering = ["created_at"]

    def to_internal_value(self, data):
        if data.get("content", None) == "":
            data.pop("content")
        return super(ContestCommentSerializer, self).to_internal_value(data)


class ContestDetailSerializer(TaggitSerializer, serializers.ModelSerializer):
    like_count = serializers.IntegerField(source="likes.count", read_only=True)
    is_liked = serializers.BooleanField(read_only=True, default=False)
    tags = TagListSerializerField()

    class Meta:
        model = Contest
        fields = "__all__"
        extra_fields = ["like_count", "is_liked", "tags"]
