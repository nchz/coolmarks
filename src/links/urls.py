from django.urls import path

from links.views import (
    list_view,
    delete_view,
    edit_view,
    update_view,
)


# app_name = "links"

urlpatterns = [
    path("", list_view, name="list"),
    path("delete/", delete_view, name="delete"),
    path("edit/", edit_view, name="edit"),
    path("update/", update_view, name="update"),
]
