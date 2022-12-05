"""
GET /links/
POST /links/
POST /links/delete/
POST /links/edit/
POST /links/update/

body = {
    # for delete, edit and update.
    "link_ids": <list of ints>,
    # only for update.
    "action": <"add", "remove" or "set">,
    "tags_string": <str>
}
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseRedirect,
)

from links.models import Link


@login_required
@require_http_methods(["GET", "POST"])
def list_view(request):
    """
    List `request.user` links on GET, create a new `Link` on POST.
    """
    if request.method == "GET":
        link_list = Link.objects.filter(owner=request.user).order_by("-dt")
        context = {
            "link_list": link_list,
        }
        return render(request, "links/index.html", context)

    elif request.method == "POST":
        if "location" not in request.POST:
            return HttpResponseBadRequest()

        location = request.POST["location"]
        tags_string = request.POST.get("tags_string", "")
        link = Link(
            owner=request.user,
            location=location,
            tags_string=tags_string,
        )
        link.save()
        return HttpResponseRedirect("/links/")


@login_required
@require_http_methods(["POST"])
def delete_view(request):
    return HttpResponse("delete_view")


@login_required
@require_http_methods(["POST"])
def edit_view(request):
    return HttpResponse("edit_view")


@login_required
@require_http_methods(["POST"])
def update_view(request):
    return HttpResponse("update_view")
