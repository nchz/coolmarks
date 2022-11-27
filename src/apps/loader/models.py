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

    def __str__(self):
        return f"({self.owner.username}) {self.title}"


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
            "id",
            "link",
            "tags_string",
            # read_only_fields
            "owner",
            "dt",
            "domain",
            "title",
            "tags",
        )

    def create(self, validated_data):
        link = validated_data["link"]

        # process link to get required values.
        try:
            r = requests.get(link)
            tree = etree.fromstring(r.text, parser=etree.HTMLParser())
            title = tree.xpath("//html/head/title")[0].text[:MAX_LENGTH]
        except (requests.exceptions.ConnectionError, IndexError, TypeError):
            title = "NO TITLE"

        domain = urlparse(link).netloc[:MAX_LENGTH]

        # create and return object.
        bookmark = Bookmark(
            owner=validated_data["owner"],
            link=link,
            domain=domain,
            title=title,
        )
        bookmark.save()

        if tags_string := validated_data["tags_string"]:
            for tag in tags_string.split(";"):
                # clean string and create tag (if any).
                tag = re.sub(r"[\s|\-|_]+", "_", tag)
                tag = re.sub(r"\W", "", tag)
                tag = re.sub(r"_+", "_", tag).strip("_")
                if tag:
                    bookmark.tags.create(label=tag)

        return bookmark
