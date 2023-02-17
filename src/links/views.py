from http import HTTPStatus

import json
from urllib.parse import urlparse

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from links.models import Link, Tag


@login_required
@require_http_methods(["GET"])
def list_view(request):
    """
    List `request.user` links.
    """
    link_list = Link.objects.filter(owner=request.user).order_by("-dt")
    context = {
        "link_list": link_list,
    }
    return render(request, "links/index.html", context)


@login_required
@require_http_methods(["POST"])
def add_view(request):
    """
    Create a new `Link` for `request.user`.
    """
    data = json.loads(request.body)

    if "location" not in data:
        return HttpResponseBadRequest()

    location = data["location"]
    link = Link.objects.filter(owner=request.user, location=location).first()

    if not link:
        title = data["title"]
        # favicon_url = data["favIconUrl"]
        _tags_string = data.get("_tags_string", "")

        link = Link(
            owner=request.user,
            location=location,
            title=title,
            # favicon_url=favicon_url,
        )
        link._tags_string = _tags_string
        link.save()
        response = {
            "message": "Link created.",
        }
        status_code = HTTPStatus.CREATED

    else:
        response = {
            "message": "Link already exists.",
        }
        status_code = HTTPStatus.CONFLICT

    # return HttpResponseRedirect(reverse("links:list"))
    return JsonResponse(response, status=status_code)


@login_required
@require_http_methods(["POST"])
def delete_view(request):
    """
    Delete links whose ids are in the requested list.
    """
    data = json.loads(request.body)

    link_ids = [int(i) for i in data.get("link_ids", "").split(",") if i != ""]
    objs = Link.objects.filter(
        pk__in=link_ids,
        owner=request.user,
    )
    objs.delete()
    response = {
        "message": "Links deleted.",
    }

    # return HttpResponseRedirect(reverse("links:list"))
    return JsonResponse(response)


@login_required
@require_http_methods(["POST"])
def edit_view(request):
    """
    Perform the requested action on the links whose ids are in the requested list.
    """
    data = json.loads(request.body)

    link_ids = [int(i) for i in data.get("link_ids", "").split(",") if i != ""]
    action = data.get("action")
    _tags_string = data.get("_tags_string", "")

    tags = Tag.from_string(_tags_string)
    if action == "set":
        tags = [tags]

    objs = Link.objects.filter(
        pk__in=link_ids,
        owner=request.user,
    )
    for o in objs:
        getattr(o.tags, action)(*tags)

    # return HttpResponseRedirect(reverse("links:list"))
    return JsonResponse({})


@login_required
@require_http_methods(["GET", "POST"])
def bulk_add_view(request):
    data = json.loads(request.body)

    if request.method == "GET":
        return render(request, "links/bulk.html")

    elif request.method == "POST":
        if "location_list" not in data:
            return HttpResponseBadRequest()

        location_list = data["location_list"]
        _tags_string = data.get("_tags_string", "")

        locations = [loc.strip() for loc in location_list.split() if loc.strip()]
        for location in locations:
            parsed_loc = urlparse(location)
            if parsed_loc.scheme and parsed_loc.netloc:
                link = Link(
                    owner=request.user,
                    location=location,
                )
                link._tags_string = _tags_string
                link.save()

        return HttpResponseRedirect(reverse("links:list"))


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def check_view(request):
    """
    Check if the requested location is in the `request.user` links.
    """
    data = json.loads(request.body)

    location = data["location"]
    try:
        link = Link.objects.get(
            location=location,
            owner=request.user,
        )
        result = {
            "link_id": link.id,
        }
    except Link.DoesNotExist:
        result = {
            "link_id": None,
        }

    return JsonResponse(result)
