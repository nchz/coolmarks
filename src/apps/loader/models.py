import re
from urllib.parse import urlparse

import requests
from lxml import etree
from django.contrib.auth.models import User
from django.db import models
from rest_framework import serializers


MAX_LENGTH = 200


class Tag(models.Model):
    label = models.CharField(max_length=MAX_LENGTH)

    def __str__(self):
        return self.label

    def bookmarks_string(self):
        return "\n".join(str(b) for b in self.bookmark_set.all())


class Bookmark(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bookmarks",
        editable=False,
    )
    dt = models.DateTimeField(auto_now_add=True)
    link = models.URLField()
    domain = models.CharField(
        max_length=MAX_LENGTH,
        editable=False,
    )
    title = models.CharField(
        max_length=MAX_LENGTH,
        editable=False,
    )
    tags = models.ManyToManyField(Tag, default=None)

    class Meta:
        ordering = ("-dt",)

    def save(self, *args, **kwargs):
        # fields aren't updated if `self.link` changes.
        if not self.title:
            # process link to get required values.
            try:
                r = requests.get(self.link)
                tree = etree.fromstring(r.text, parser=etree.HTMLParser())
                self.title = tree.xpath("//html/head/title")[0].text[:MAX_LENGTH]
            except (requests.exceptions.ConnectionError, IndexError, TypeError):
                self.title = "NO TITLE"
            self.domain = urlparse(self.link).netloc[:MAX_LENGTH]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} ({self.owner.username}) {self.title}"


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
            tag = re.sub(r"[\s|\-|_]+", "_", tag)
            tag = re.sub(r"\W", "", tag)
            tag = re.sub(r"_+", "_", tag).strip("_").replace("_", "-")
            if tag != "":
                tags.add(tag)
        return tags
