import re
from urllib.parse import urlparse

from django.contrib.auth.models import User
from django.db import models

import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


MAX_LENGTH = 200
CHROMEDRIVER_PATH = "/src/chromedriver"
driver_options = Options()
driver_options.headless = True


class Tag(models.Model):
    name = models.CharField(max_length=MAX_LENGTH)

    @classmethod
    def from_string(cls, tags_string):
        """
        Return a list of Tag instances which names come from `tags_string`.
        """
        tags = cls._parse_tags(tags_string)
        return [cls.objects.get_or_create(name=t)[0] for t in tags]

    @staticmethod
    def _parse_tags(tags_string):
        tags = set()
        for tag in tags_string.split(";"):
            tag = re.sub(r"[\s|\-|_]+", "_", tag)
            tag = re.sub(r"\W", "", tag)
            tag = re.sub(r"_+", "_", tag).strip("_")
            tag = tag.replace("_", "-").lower()
            if tag != "":
                tags.add(tag)
        return tags

    def __str__(self):
        return f"[{self.id}] {self.name}"

    def links_string(self):
        return "\n".join(str(link) for link in self.link_set.all())


class Link(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        # related_name="links",
        editable=False,
    )
    dt = models.DateTimeField(auto_now_add=True)
    location = models.URLField()
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
        # fields aren't updated if `self.location` changes.
        if not self.title:
            # process link to get required values.
            try:
                r = requests.get(self.location)
                tree = etree.fromstring(r.text, parser=etree.HTMLParser())
                title = tree.xpath("//html/head/title")[0].text[:MAX_LENGTH]
            except (requests.exceptions.ConnectionError, IndexError, TypeError):
                driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=driver_options)
                driver.get(self.location)
                title = driver.title
                driver.quit()
            except Exception:
                title = self.location

            self.title = title
            self.domain = urlparse(self.location).netloc[:MAX_LENGTH]
            super().save(*args, **kwargs)
            # tags_string = "; ".join(t.name for t in link.tags.all())
            self.tags.set(Tag.from_string(self.tags_string), clear=True)

    def __str__(self):
        return f"[{self.id}; {self.owner.username}] {self.location} -- {self.title}"
