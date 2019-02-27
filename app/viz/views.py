import os
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from . import forms
from PIL import Image
from .core.sna import *
from .core.wc import *


def sna_interactive(request):
    if request.method == 'POST':
        form = forms.SnaInteractiveForm(request.POST)
        if form.is_valid():
            options = form.cleaned_data
            theme = options.pop('theme')
            value_error, footer_sticky = False, True

            try:
                partition_data = gen_gexf_and_pass_partition_data(**options)
            except ValueError:
                value_error, footer_sticky = True, False

            context = {
                'theme': theme,
                'value_error': value_error,
                'footer_sticky': footer_sticky,
                'partition_data': partition_data,
            }
            return render(request, 'viz/show_result/sna_interactive.html', context)
    else:
        form = forms.SnaInteractiveForm()
    return render(request, 'viz/default/sna_interactive-config.html', {'form': form})


def wc(request):
    if request.method == 'POST':
        form = forms.WcForm(request.POST, request.FILES)
        if form.is_valid():
            options = form.cleaned_data
            value_error, footer_sticky = False, True

            try:
                make_wc_png(**options)
            except ValueError:
                value_error, footer_sticky = True, False

            context = {
                'value_error': value_error,
                'footer_sticky': footer_sticky,
            }
            return render(request, 'viz/show_result/wc.html', context)
    else:
        form = forms.WcForm()
    return render(request, 'viz/default/wc-config.html', {'form': form})


# -- Visualization From File -- #
def sna_interactive_file(request):
    if request.method == 'POST':
        form = forms.SnaInteractiveFileForm(request.POST, request.FILES)
        if form.is_valid():
            options = form.cleaned_data
            theme = options.pop('theme')
            value_error, footer_sticky = False, True

            try:
                partition_data = gen_gexf_and_pass_partition_data(**options)
            except ValueError:
                value_error, footer_sticky = True, False

            context = {
                'theme': theme,
                'value_error': value_error,
                'footer_sticky': footer_sticky,
                'partition_data': partition_data,
            }
            return render(request, 'viz/show_result/sna_interactive.html', context)
    else:
        form = forms.SnaInteractiveFileForm()
    return render(request, 'viz/file/sna_interactive-config.html', {'form': form})


def wc_file(request):
    if request.method == 'POST':
        form = forms.WcFileForm(request.POST, request.FILES)
        if form.is_valid():
            options = form.cleaned_data
            value_error, footer_sticky = False, True

            try:
                make_wc_png(**options)
            except ValueError:
                value_error, footer_sticky = True, False

            context = {
                'value_error': value_error,
                'footer_sticky': footer_sticky,
            }
            return render(request, 'viz/show_result/wc.html', context)
    else:
        form = forms.WcFileForm()
    return render(request, 'viz/file/wc-config.html', {'form': form})


# -- Get Result --#
def get_gexf(request):
    result = open(os.path.join(settings.ROOT_DIR, '.viz_raw/sna_gexf.gexf')).read()
    return HttpResponse(result, content_type='text/xml')


def wc_result(request):
    result = Image.open(os.path.join(settings.ROOT_DIR, '.viz_raw/wc.png'))
    response = HttpResponse(content_type="image/png")
    result.save(response, 'png')
    return response
