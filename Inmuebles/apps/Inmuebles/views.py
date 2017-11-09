# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.template import loader
from django.db.models import Q
from django.shortcuts import render_to_response
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView

from .models import InmuebleTipo, Inmueble
from .forms import InmuebleTipoForm


def index(request):
    template = loader.get_template('index.html')
    context = {
        'title': 'Inmuebles',
    }
    return HttpResponse(template.render(context, request))


class InmueblesListView(ListView):
    model = Inmueble
    template_name = 'Inmueble/IListar.html'
    paginate_by = 25

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            qset = (
                Q(IDescripcion__icontains=query) |
                Q(ITipo__ITDescripcion__icontains=query) |
                Q(ITipo__ITDescripcion_Corta__icontains=query)
            )
            results = Inmueble.objects.filter(qset).distinct()
        else:
            results = Inmueble.objects.all()
        return results


class InmuebleTipoListView(ListView):
    model = InmuebleTipo
    template_name = 'InmuebleTipo/ITListar.html'

    def get_context_data(self, **kwargs):
        context = super(InmuebleTipoListView, self).get_context_data(**kwargs)
        context['title'] = 'Tipos de Inmuebles'
        context['date'] = timezone.now().date
        return context


class InmuebleTipoCreateView(CreateView):
    model = InmuebleTipo
    fields = ['ITDescripcion', 'ITDescripcion_Corta']
    template_name = 'InmuebleTipo/ITAgregar.html'
    success_url = reverse_lazy('Inmuebles:listarInmuebleTipo')
