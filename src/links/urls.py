from django.urls import path

from links import views


app_name = "links"

urlpatterns = [
    path("", views.list_view, name="list"),
    path("add/", views.add_view, name="add"),
    path("delete/", views.delete_view, name="delete"),
    path("edit/", views.edit_view, name="edit"),
    path("bulk/", views.bulk_add_view, name="bulk_add"),
    path("check/", views.check_view, name="check"),
]
