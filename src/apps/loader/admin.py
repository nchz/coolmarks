from django.contrib import admin

from apps.loader.models import Bookmark


class BookmarkAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Bookmark._meta.get_fields()]
    readonly_fields = (
        "owner",
        "dt",
    )


admin.site.register(Bookmark, BookmarkAdmin)
