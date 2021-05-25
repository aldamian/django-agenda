from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.db.models import Q

# Relative import
from .forms import AgendaModelForm
from .models import Agenda


@login_required
def search_view(request, *args, **kwargs):
    query = request.GET.get('q')
    qs = Agenda.objects.filter(title__icontains=query[0])
    print(query, qs)
    context = {"name": "Damian", "query": query}
    return render(request, "home.html", context)


@login_required
def agenda_create_view(request, *args, **kwargs):

    form = AgendaModelForm(request.POST or None, request=request)
    if form.is_valid():
        obj = form.save(commit=False)
        """
        do some stuff with it and then save into database
        stuff to do with it
        """
        obj.user = request.user
        obj.save()
        # cleaned data = validated data
        # print(form.cleaned_data)
        # data = form.cleaned_data
        # Agenda.objects.create(**data)
        form = AgendaModelForm(request=request)
        # return HttpResponseRedirect("/success")
        # return redirect("/success")
    return render(request, "agenda/create_agenda.html", {"form": form})


def agenda_detail_view(request, pk):
    try:
        obj = Agenda.objects.get(pk=pk)
    except Agenda.DoesNotExist:
        raise Http404
    # return HttpResponse(f"Product id {obj.id}")
    if request.user == obj.user or obj.public == 1:
        return render(request, "agenda/agenda_detail.html", {"object": obj})
    else:
        return HttpResponseNotFound("Page not found.")


# @staff_member_required
def agenda_list_view(request, *args, **kwargs):
    if request.user.is_anonymous:
        qs = Agenda.objects.filter(public=1)
    else:
        qs = Agenda.objects.filter(Q(user=request.user) | Q(public=1))

    context = {"object_list": qs}
    return render(request, "agenda/list.html", context)


def agenda_api_detail_view(request, pk, *args, **kwargs):
    try:
        obj = Agenda.objects.get(pk=pk)
    except Agenda.DoesNotExist:
        # return JSON with HTTP status code of 404
        return JsonResponse({"message": "Not found"})
    return JsonResponse({"id": obj.id})
