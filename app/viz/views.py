from django.shortcuts import render
from . import forms
from .core.sna import *
from .core.wc import *


def sna_interactive(request):
    if request.method == 'POST':
        form = forms.SnaInteractiveForm(request.POST, request.FILES)
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
            return render(request, 'viz/viz_result_pages/sna_interactive.html', context)
    else:
        form = forms.SnaInteractiveForm()
    return render(request, 'viz/viz_configs/sna_interactive.html', {'form': form})


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
