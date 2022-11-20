from django.contrib.auth.models import User
from django.db import models
from rest_framework import serializers


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
        max_length=100,
    )
    title = models.CharField(
        editable=False,
        max_length=300,
    )


# TODO HyperlinkedModelSerializer
class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        exclude = (
            "id",
            "owner",
        )
