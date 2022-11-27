import re

from rest_framework import serializers

from apps.loader.models import Bookmark, MAX_LENGTH


class BookmarkSerializer(serializers.ModelSerializer):
    # tags = TagSerializer(many=True, read_only=False)
    tags_string = serializers.CharField(
        max_length=MAX_LENGTH,
        default="",
        write_only=True,
    )

    class Meta:
        model = Bookmark
        depth = 1
        fields = (
            "link",
            "tags_string",
            # read_only_fields
            "id",
            "owner",
            "dt",
            "domain",
            "title",
            "tags",
        )

    def to_representation(self, instance):
        r = super().to_representation(instance)
        r["tags_string"] = "; ".join(t.label for t in instance.tags.all())
        return r

    def create(self, validated_data):
        tags = self._get_tags(validated_data.pop("tags_string"))
        instance = super().create(validated_data)
        for tag in tags:
            instance.tags.create(label=tag)
        return instance

    def update(self, instance, validated_data):
        tags = self._get_tags(validated_data.pop("tags_string"))
        instance = super().update(instance, validated_data)
        instance.tags.clear()
        for tag in tags:
            instance.tags.create(label=tag)
        return instance

    @staticmethod
    def _get_tags(tags_string):
        tags = set()
        for tag in tags_string.split(";"):
            # TODO may be part of Tag model.
            tag = re.sub(r"[\s|\-|_]+", "_", tag)
            tag = re.sub(r"\W", "", tag)
            tag = re.sub(r"_+", "_", tag).strip("_").replace("_", "-")
            if tag != "":
                tags.add(tag)
        return tags
