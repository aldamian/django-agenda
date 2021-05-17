from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render

# Relative import
from .models import Agenda


def home_view(request, *args, **kwargs):
    context = {"name": "Damian"}
    return render(request, "home.html", context)


def agenda_detail_view(request, pk):
    try:
        obj = Agenda.objects.get(pk=pk)
    except Agenda.DoesNotExist:
        # render html page, with HTTP status code of 404
        raise Http404
    # return HttpResponse(f"Product id {obj.id}")
    """
    TODO     replace title with content
    """
    return render(request, "agendas/detail.html", {"object": obj})


def agenda_api_detail_view(request, pk, *args, **kwargs):
    try:
        obj = Agenda.objects.get(pk=pk)
    except Agenda.DoesNotExist:
        # return JSON with HTTP status code of 404
        return JsonResponse({"message": "Not found"})
    return JsonResponse({"id": obj.id})
