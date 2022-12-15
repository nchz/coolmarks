from django.urls import path

from links import views


app_name = "links"

urlpatterns = [
    path("", views.list_view, name="list"),
    path("delete/", views.delete_view, name="delete"),
    path("edit/", views.edit_view, name="edit"),
    path("update/", views.update_view, name="update"),
]
