from urllib.parse import urlparse

import requests
from lxml import etree
from django.contrib.auth.models import User
from django.db import models
from rest_framework import serializers


MAX_LENGTH = 200


class Bookmark(models.Model):
    owner = models.ForeignKey(
        User,
        editable=False,
        on_delete=models.CASCADE,
        related_name="bookmarks",
    )
    dt = models.DateTimeField(
        auto_now_add=True,
    )
    link = models.URLField()
    domain = models.CharField(
        editable=False,
        max_length=MAX_LENGTH,
    )
    title = models.CharField(
        editable=False,
        max_length=MAX_LENGTH,
    )


# TODO HyperlinkedModelSerializer
class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        exclude = (
            "id",
            "owner",
        )

    def create(self, validated_data):
        link = validated_data["link"]

        # process link to get required values.
        domain = urlparse(link).netloc[:MAX_LENGTH]

        r = requests.get(link)
        tree = etree.fromstring(r.text, parser=etree.HTMLParser())
        try:
            title = tree.xpath("//html/head/title")[0].text[:MAX_LENGTH]
        except (IndexError, TypeError):
            title = "NO TITLE"

        # create and return object.
        bookmark = Bookmark(
            owner=validated_data["owner"],
            link=link,
            domain=domain,
            title=title,
        )
        bookmark.save()
        return bookmark
