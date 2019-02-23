from PIL import Image
from django.conf import settings
import os
from django.http import HttpResponse
from django.shortcuts import render
from . import forms
from .core.sna import *
from .core.wc import *


def sna_interactive(request):
    if request.method == 'POST':
        form = forms.SnaInteractiveForm(request.POST)
        if form.is_valid():
            options = {
                'data': form.cleaned_data['data'] or open(os.path.join(settings.ROOT_DIR, 'sample_data.txt'), 'rt').read(),
                'edge_remove_threshold': form.cleaned_data['edge_remove_threshold'],
                'node_num': int(form.cleaned_data['node_num']),
                'sw': form.cleaned_data['stopwords'],
                'remove_isolated_node': form.cleaned_data['remove_isolated_node'],
                'layout': form.cleaned_data['layout'],
                'iterations': form.cleaned_data['iterations'],
                'fr_k': form.cleaned_data['fr_k'] or None,
                'fa2_option': (form.cleaned_data['fa2_square'], form.cleaned_data['fa2_log_base']),
            }
            value_error = False
            footer_sticky = True
            try:
                make_sna_gexf(**options)
            except ValueError:
                value_error = True
                footer_sticky = False
            return render(request, 'viz/show_result/sna_interactive.html',
                          {
                              'theme': form.cleaned_data['theme'],
                              'footer_sticky': footer_sticky,
                              'value_error': value_error
                          })
    else:
        form = forms.SnaInteractiveForm
    return render(request, 'viz/default/sna_interactive-config.html', {'form': form})


def sna(request):
    if request.method == 'POST':
        form = forms.SnaForm(request.POST)
        if form.is_valid():
            options = {
                'data': form.cleaned_data['data'] or open(os.path.join(settings.ROOT_DIR, 'sample_data.txt'), 'rt').read(),
                'edge_remove_threshold': form.cleaned_data['edge_remove_threshold'],
                'node_num': int(form.cleaned_data['node_num']),
                'sw': form.cleaned_data['stopwords'],
                'remove_isolated_node': form.cleaned_data['remove_isolated_node'],
                'layout': form.cleaned_data['layout'],
                'iterations': form.cleaned_data['iterations'],
                'fr_k': form.cleaned_data['fr_k'] or None,
                'fa2_option': (form.cleaned_data['fa2_square'], form.cleaned_data['fa2_log_base']),
            }
            value_error = False
            footer_sticky = True
            try:
                make_sna_png(**options)
            except(ValueError, KeyError):
                value_error = True
                footer_sticky = False
            return render(request, 'viz/show_result/sna.html',
                          {'footer_sticky': footer_sticky, 'value_error': value_error})
    else:
        form = forms.SnaForm
    return render(request, 'viz/default/sna-config.html', {'form': form})


def wc(request):
    if request.method == 'POST':
        form = forms.WcForm(request.POST, request.FILES)
        if form.is_valid():
            options = {
                'data': form.cleaned_data['data'] or open(os.path.join(settings.ROOT_DIR, 'sample_data.txt'), 'rt').read(),
                'sw': form.cleaned_data['stopwords'],
                'max_word_size': form.cleaned_data['max_word_size'],
                'bg_color': form.cleaned_data['bg_color'],
                'font': form.cleaned_data['font'],
                'mask': form.cleaned_data['mask'],
                'mask_coloring': form.cleaned_data['mask_coloring'],
            }
            value_error = False
            footer_sticky = True
            try:
                make_wc_png(**options)
            except ValueError:
                value_error = True
                footer_sticky = False
            return render(request, 'viz/show_result/wc.html',
                          {'footer_sticky': footer_sticky, 'value_error': value_error})
    else:
        form = forms.WcForm
    return render(request, 'viz/default/wc-config.html', {'form': form})


# -- Visualization From File -- #
def sna_interactive_file(request):
    if request.method == 'POST':
        form = forms.SnaInteractiveFileForm(request.POST, request.FILES)
        if form.is_valid():
            options = {
                'data': form.cleaned_data['data'],
                'edge_remove_threshold': form.cleaned_data['edge_remove_threshold'],
                'node_num': int(form.cleaned_data['node_num']),
                'sw': form.cleaned_data['stopwords'],
                'remove_isolated_node': form.cleaned_data['remove_isolated_node'],
                'layout': form.cleaned_data['layout'],
                'iterations': form.cleaned_data['iterations'],
                'fr_k': form.cleaned_data['fr_k'] or None,
                'fa2_option': (form.cleaned_data['fa2_square'], form.cleaned_data['fa2_log_base']),
            }
            value_error = False
            footer_sticky = True
            try:
                make_sna_gexf(**options)
            except ValueError:
                value_error = True
                footer_sticky = False
            return render(request, 'viz/show_result/sna_interactive.html',
                          {
                              'theme': form.cleaned_data['theme'],
                              'footer_sticky': footer_sticky,
                              'value_error': value_error,
                              'mode_file': True,
                          })
    else:
        form = forms.SnaInteractiveFileForm
    return render(request, 'viz/file/sna_interactive-config.html', {'form': form})


def sna_file(request):
    if request.method == 'POST':
        form = forms.SnaFileForm(request.POST, request.FILES)
        if form.is_valid():
            options = {
                'data': form.cleaned_data['data'],
                'edge_remove_threshold': form.cleaned_data['edge_remove_threshold'],
                'node_num': int(form.cleaned_data['node_num']),
                'sw': form.cleaned_data['stopwords'],
                'remove_isolated_node': form.cleaned_data['remove_isolated_node'],
                'layout': form.cleaned_data['layout'],
                'iterations': form.cleaned_data['iterations'],
                'fr_k': form.cleaned_data['fr_k'] or None,
                'fa2_option': (form.cleaned_data['fa2_square'], form.cleaned_data['fa2_log_base']),
            }
            value_error = False
            footer_sticky = True
            try:
                make_sna_png(**options)
            except(ValueError, KeyError):
                value_error = True
                footer_sticky = False
            return render(request, 'viz/show_result/sna.html',
                          {'footer_sticky': footer_sticky, 'value_error': value_error, 'mode_file': True})
    else:
        form = forms.SnaFileForm
    return render(request, 'viz/file/sna-config.html', {'form': form})


def wc_file(request):
    if request.method == 'POST':
        form = forms.WcFileForm(request.POST, request.FILES)
        if form.is_valid():
            options = {
                'data': form.cleaned_data['data'],
                'sw': form.cleaned_data['stopwords'],
                'max_word_size': form.cleaned_data['max_word_size'],
                'bg_color': form.cleaned_data['bg_color'],
                'font': form.cleaned_data['font'],
                'mask': form.cleaned_data['mask'],
                'mask_coloring': form.cleaned_data['mask_coloring'],
            }
            value_error = False
            footer_sticky = True
            try:
                make_wc_png(**options)
            except ValueError:
                value_error = True
                footer_sticky = False
            return render(request, 'viz/show_result/wc.html',
                          {'footer_sticky': footer_sticky, 'value_error': value_error, 'mode_file': True})
    else:
        form = forms.WcFileForm
    return render(request, 'viz/file/wc-config.html', {'form': form})

# -- Get Result --#
def get_gexf(request):
    result = open(os.path.join(settings.ROOT_DIR, '.viz_raw/sna_gexf.gexf')).read()
    return HttpResponse(result, content_type='text/xml')


def sna_result(request):
    result = Image.open(os.path.join(settings.ROOT_DIR, '.viz_raw/sna.png'))
    response = HttpResponse(content_type="image/png")
    result.save(response, 'png')
    return response


def wc_result(request):
    result = Image.open(os.path.join(settings.ROOT_DIR, '.viz_raw/wc.png'))
    response = HttpResponse(content_type="image/png")
    result.save(response, 'png')
    return response
