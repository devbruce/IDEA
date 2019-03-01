from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from . import forms
from .core.sna import *
from .core.wc import *
from PIL import Image
import os
import networkx as nx


def sna(request):
    if request.method == 'POST':
        form = forms.SnaForm(request.POST, request.FILES)
        if form.is_valid():
            options = form.cleaned_data
            theme = options.pop('theme')
            errors, footer_sticky = False, True
            value_error, memory_error = False, False

            try:
                partition_data = gen_gexf_and_pass_partition_data(**options)
            except ValueError:
                errors, footer_sticky = True, False
                value_error = True
            except nx.NetworkXError:
                errors, footer_sticky = True, False
                memory_error = True

            context = {
                'theme': theme,
                'errors': errors,
                'footer_sticky': footer_sticky,
                'value_error': value_error,
                'memory_error': memory_error,
            }
            if not errors:
                context['partition_data'] = partition_data
            return render(request, 'viz/viz_result_pages/sna.html', context)
    else:
        form = forms.SnaForm()
    return render(request, 'viz/viz_configs/sna.html', {'form': form})


def wc(request):
    if request.method == 'POST':
        form = forms.WcForm(request.POST, request.FILES)
        if form.is_valid():
            options = form.cleaned_data
            errors, footer_sticky = False, True

            try:
                gen_wc_png(**options)
            except ValueError:
                errors, footer_sticky = True, False

            context = {
                'errors': errors,
                'footer_sticky': footer_sticky,
            }
            return render(request, 'viz/viz_result_pages/wc.html', context)
    else:
        form = forms.WcForm()
    return render(request, 'viz/viz_configs/wc.html', {'form': form})


# -- Get Result Files --#
def get_sna_gexf(request):
    result = open(os.path.join(settings.VIZ_DIR, 'sna.gexf')).read()
    return HttpResponse(result, content_type='text/xml')


def get_wc_png(request):
    result = Image.open(os.path.join(settings.VIZ_DIR, 'wc.png'))
    response = HttpResponse(content_type="image/png")
    result.save(response, 'png')
    return response
