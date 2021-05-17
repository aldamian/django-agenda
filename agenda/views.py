from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render, redirect

# Relative import
from .forms import AgendaModelForm
from .models import Agenda


def search_view(request, *args, **kwargs):
    query = request.GET.get('q')
    qs = Agenda.objects.filter(title__icontains=query[0])
    print(query, qs)
    context = {"name": "Damian", "query": query}
    return render(request, "home.html", context)


""" 
THIS IS BAD.
THIS IS HARD CODED
"""
# def agenda_create_view(request, *args, **kwargs):
#     # print(request.POST)
#     # print(request.GET)
#     if request.method == "POST":
#         post_data = request.POST or None
#         if post_data is not None:
#             my_form = AgendaForm(request.POST)
#             if my_form.is_valid():
#                 print(my_form.cleaned_data.get("title"))
#                 title_from_input = my_form.cleaned_data.get("title")
#                 Agenda.objects.create(title=title_from_input)
#                 # print("post data", post_data)
#
#     return render(request, "forms.html", {})


def agenda_create_view(request, *args, **kwargs):
    form = AgendaModelForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        # do some stuff with it and then save into database
        """
        stuff to do with it
        obj.user = request.user
        """
        obj.save()
        # cleaned data = validated data
        # print(form.cleaned_data)
        # data = form.cleaned_data
        # Agenda.objects.create(**data)
        form = AgendaModelForm()
        # return HttpResponseRedirect("/success")
        # return redirect("/success")
    return render(request, "forms.html", {"form": form})


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
    return render(request, "agendas/agenda_detail.html", {"object": obj})


def agenda_list_view(request, *args, **kwargs):
    qs = Agenda.objects.all()  # query set
    context = {"object_list": qs}
    return render(request, "agendas/list.html", context)


def agenda_api_detail_view(request, pk, *args, **kwargs):
    try:
        obj = Agenda.objects.get(pk=pk)
    except Agenda.DoesNotExist:
        # return JSON with HTTP status code of 404
        return JsonResponse({"message": "Not found"})
    return JsonResponse({"id": obj.id})
