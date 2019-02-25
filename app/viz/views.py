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
                'word_len_min': form.cleaned_data['word_len_min'],
                'stopwords': form.cleaned_data['stopwords'],
                'remove_isolated_node': form.cleaned_data['remove_isolated_node'],
                'layout': form.cleaned_data['layout'],
                'iterations': form.cleaned_data['iterations'],
                'fr_k': form.cleaned_data['fr_k'] or None,
                'fa2_option': (form.cleaned_data['fa2_square'], form.cleaned_data['fa2_log_base']),
            }
            value_error, footer_sticky = False, True

            try:
                make_sna_gexf(**options)
            except ValueError:
                value_error, footer_sticky = True, False

            context = {
                'theme': form.cleaned_data['theme'],
                'value_error': value_error,
                'footer_sticky': footer_sticky,
            }
            return render(request, 'viz/show_result/sna_interactive.html', context)
    else:
        form = forms.SnaInteractiveForm()
    return render(request, 'viz/default/sna_interactive-config.html', {'form': form})


def sna(request):
    if request.method == 'POST':
        form = forms.SnaForm(request.POST)
        if form.is_valid():
            options = {
                'data': form.cleaned_data['data'] or open(os.path.join(settings.ROOT_DIR, 'sample_data.txt'), 'rt').read(),
                'edge_remove_threshold': form.cleaned_data['edge_remove_threshold'],
                'node_num': int(form.cleaned_data['node_num']),
                'word_len_min': form.cleaned_data['word_len_min'],
                'stopwords': form.cleaned_data['stopwords'],
                'remove_isolated_node': form.cleaned_data['remove_isolated_node'],
                'layout': form.cleaned_data['layout'],
                'iterations': form.cleaned_data['iterations'],
                'fr_k': form.cleaned_data['fr_k'] or None,
                'fa2_option': (form.cleaned_data['fa2_square'], form.cleaned_data['fa2_log_base']),
            }
            value_error, footer_sticky = False, True

            try:
                make_sna_png(**options)
            except(ValueError, KeyError):
                value_error, footer_sticky = True, False

            context = {
                'value_error': value_error,
                'footer_sticky': footer_sticky,
            }
            return render(request, 'viz/show_result/sna.html', context)
    else:
        form = forms.SnaForm()
    return render(request, 'viz/default/sna-config.html', {'form': form})


def wc(request):
    if request.method == 'POST':
        form = forms.WcForm(request.POST, request.FILES)
        if form.is_valid():
            options = form.cleaned_data
            if not options['data']:
                options['data'] = open(os.path.join(settings.ROOT_DIR, 'sample_data.txt'), 'rt').read()
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
            options = {
                'data': form.cleaned_data['data'],
                'edge_remove_threshold': form.cleaned_data['edge_remove_threshold'],
                'node_num': int(form.cleaned_data['node_num']),
                'word_len_min': form.cleaned_data['word_len_min'],
                'stopwords': form.cleaned_data['stopwords'],
                'remove_isolated_node': form.cleaned_data['remove_isolated_node'],
                'layout': form.cleaned_data['layout'],
                'iterations': form.cleaned_data['iterations'],
                'fr_k': form.cleaned_data['fr_k'] or None,
                'fa2_option': (form.cleaned_data['fa2_square'], form.cleaned_data['fa2_log_base']),
            }
            value_error, footer_sticky = False, True

            try:
                make_sna_gexf(**options)
            except ValueError:
                value_error, footer_sticky = True, False

            context = {
                'theme': form.cleaned_data['theme'],
                'value_error': value_error,
                'footer_sticky': footer_sticky,
                'mode_file': True,
            }
            return render(request, 'viz/show_result/sna_interactive.html', context)
    else:
        form = forms.SnaInteractiveFileForm()
    return render(request, 'viz/file/sna_interactive-config.html', {'form': form})


def sna_file(request):
    if request.method == 'POST':
        form = forms.SnaFileForm(request.POST, request.FILES)
        if form.is_valid():
            options = {
                'data': form.cleaned_data['data'],
                'edge_remove_threshold': form.cleaned_data['edge_remove_threshold'],
                'node_num': int(form.cleaned_data['node_num']),
                'word_len_min': form.cleaned_data['word_len_min'],
                'stopwords': form.cleaned_data['stopwords'],
                'remove_isolated_node': form.cleaned_data['remove_isolated_node'],
                'layout': form.cleaned_data['layout'],
                'iterations': form.cleaned_data['iterations'],
                'fr_k': form.cleaned_data['fr_k'] or None,
                'fa2_option': (form.cleaned_data['fa2_square'], form.cleaned_data['fa2_log_base']),
            }
            value_error, footer_sticky = False, True

            try:
                make_sna_png(**options)
            except(ValueError, KeyError):
                value_error, footer_sticky = True, False

            context = {
                'value_error': value_error,
                'footer_sticky': footer_sticky,
                'mode_file': True,
            }
            return render(request, 'viz/show_result/sna.html', context)
    else:
        form = forms.SnaFileForm()
    return render(request, 'viz/file/sna-config.html', {'form': form})


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
                'mode_file': True,
            }
            return render(request, 'viz/show_result/wc.html', context)
    else:
        form = forms.WcFileForm()
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
