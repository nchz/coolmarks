from django.contrib import admin

from apps.loader.models import Bookmark, Tag


class BookmarkAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Bookmark._meta.get_fields()[:-1]]
    readonly_fields = (
        "id",
        "owner",
        "dt",
        "tags",
    )


class TagAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "label",
    )
    readonly_fields = (
        "id",
        "bookmarks_string",
    )


admin.site.register(Bookmark, BookmarkAdmin)
admin.site.register(Tag, TagAdmin)
