from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from . import forms
from .core.sna import *
from .core.wc import *
from PIL import Image
import os


def sna(request):
    if request.method == 'POST':
        form = forms.SnaForm(request.POST, request.FILES)
        if form.is_valid():
            options = form.cleaned_data
            theme = options.pop('theme')
            value_error, footer_sticky = False, True

            try:
                partition_data = gen_gexf_and_pass_partition_data(**options)
            except FileNotFoundError:
                value_error, footer_sticky = True, False

            context = {
                'theme': theme,
                'value_error': value_error,
                'footer_sticky': footer_sticky,
            }
            if not value_error:
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
            value_error, footer_sticky = False, True

            try:
                gen_wc_png(**options)
            except ValueError:
                value_error, footer_sticky = True, False

            context = {
                'value_error': value_error,
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
