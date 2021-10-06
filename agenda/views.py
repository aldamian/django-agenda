from django.contrib.auth.decorators import login_required
# from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse, Http404, HttpResponseNotFound
# from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render  # , redirect
from django.db.models import Q

# PDF file

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

# from io import BytesIO
# from datetime import date

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
        """
        cleaned data = validated data
        print(form.cleaned_data)
        data = form.cleaned_data
        Agenda.objects.create(**data)
        """
        form = AgendaModelForm(request=request)
        """
        return HttpResponseRedirect("/success")
        return redirect("/success")        
        """

    return render(request, "agenda/agenda_create.html", {"form": form})


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


@login_required
def agenda_render_pdf_view(request, pk):
    try:
        agenda = Agenda.objects.get(pk=pk)
    except Agenda.DoesNotExist:
        raise Http404

    template_path = 'pdf/agenda_entry_pdf.html'
    context = {'agenda': agenda}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    filename = agenda.title + '.pdf'
    # if download
    # response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
    # if display
    response['Content-Disposition'] = 'filename="{}"'.format(filename)
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def agenda_list_view(request, *args, **kwargs):
    if request.user.is_anonymous:
        qs = Agenda.objects.filter(public=1).order_by('-last_modified', 'entry_date')
    else:
        qs = Agenda.objects.filter(Q(user=request.user) | Q(public=1)).order_by('-last_modified', 'entry_date')

    context = {"object_list": qs}
    return render(request, "agenda/agenda_list.html", context)


@login_required
def agenda_calendar_view(request):
    qs = Agenda.objects.filter(user=request.user)

    context = {"agenda_list": qs}
    for agenda in qs:
        agenda.entry_date = str(agenda.entry_date)
    # how do I make an event occupy the entire cell?
    return render(request, 'agenda/agenda_calendar_view.html', context)


@login_required
def search_agenda_view(request):
    if request.method == "POST":
        searched = request.POST.get('searched')
        qs = Agenda.objects.filter(Q(user=request.user) | Q(public=1))\
                           .filter(tags__icontains=searched)\
                           .order_by('-last_modified', 'entry_date')
        """
        SEARCH BY TAGS SHOULD APPEAR IN THE SAME PAGE. Dynamically update the page? How?
            - ajax
            
        refresh page but different results based on search
        """
        return render(request, 'agenda/agenda_search_by_tags.html',
                      {'searched': searched,
                       'agenda': qs})
    else:
        return render(request, 'agenda/agenda_search_by_tags.html', {})


def agenda_api_detail_view(request, pk, *args, **kwargs):
    try:
        obj = Agenda.objects.get(pk=pk)
    except Agenda.DoesNotExist:
        # return JSON with HTTP status code of 404
        return JsonResponse({"message": "Not found"})
    return JsonResponse({"id": obj.id})
