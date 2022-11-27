from urllib.parse import urlparse

import requests
from lxml import etree
from django.contrib.auth.models import User
from django.db import models


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
        return f"{self.id} ({self.owner.username}) {self.link} -- {self.title}"
