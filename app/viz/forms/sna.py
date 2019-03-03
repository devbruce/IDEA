from django import forms
from .base import VizBaseForm
import pandas as pd


class SnaForm(VizBaseForm):
    network_size = (
        (35, 'Small (35)'),
        (60, 'Regular (60)'),
        (100, 'Large (100)'),
    )
    theme_list = (
        ('default', 'Default'),
        ('light', 'Light'),
        ('dark', 'Dark'),
    )
    layouts = (
        ('fr', 'Fruchterman Reingold'),
        ('fa2', 'ForceAtlas2'),
    )
    theme = forms.ChoiceField(
        required=True,
        choices=theme_list,
        initial='default',
    )
    node_num = forms.ChoiceField(
        required=True,
        label='Network Size',
        choices=network_size,
        initial=35,
        help_text='Number of nodes',
    )
    edge_remove_threshold = forms.IntegerField(
        required=True,
        label='Edge Remove Threshold',
        initial=0,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control mb-1',
            }
        ),
    )
    remove_isolated_node = forms.BooleanField(
        required=False,
        label='Remove Isolated Node',
        initial=True,
        help_text='Default : ON',
    )
    iterations = forms.IntegerField(
        required=True,
        initial=50,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    layout = forms.ChoiceField(
        required=True,
        choices=layouts,
        initial='fr',
    )
    fr_k = forms.IntegerField(
        required=True,
        label='Variable k',
        initial=1,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control mb-1'
            }
        ),
        help_text='As the value increases, the distance of the node increases. '
                  'Default 0 equals None',
    )
    fa2_square = forms.IntegerField(
        required=True,
        label='Variable Square',
        initial=2,
    )
    fa2_log_base = forms.IntegerField(
        required=True,
        label='Variable log(base)',
        initial=100,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control mb-1'
            }
        ),
    )

    def clean_data_file(self):
        uploaded_data = self.cleaned_data['data_file']
        if uploaded_data:
            if uploaded_data.content_type == 'text/plain':
                data_raw = uploaded_data.read().decode()
                return data_raw.split('\n')
            elif uploaded_data.content_type == 'text/csv':
                data_raw = pd.read_csv(uploaded_data, encoding='CP949', header=None)
                data = []
                for post in data_raw[0]:
                    data.append(post)
                return data
            else:
                self.fields['data_file'].widget.attrs['class'] += ' is-invalid'
                raise forms.ValidationError("Uploaded File is not *.txt or *.csv")
        else:
            return None

    def clean_node_num(self):
        node_num = self.cleaned_data['node_num']
        return int(node_num)

    def clean_edge_remove_threshold(self):
        edge_remove_threshold = self.cleaned_data['edge_remove_threshold']
        if edge_remove_threshold < 0:
            self.fields['edge_remove_threshold'].widget.attrs['class'] += ' is-invalid'
            raise forms.ValidationError("Edge Remove Threshold can't be negative")
        return edge_remove_threshold

    def clean_iterations(self):
        iterations = self.cleaned_data['iterations']
        if iterations < 0:
            self.fields['iterations'].widget.attrs['class'] += ' is-invalid'
            raise forms.ValidationError("Iterations can't be negative")
        return iterations

    def clean_fr_k(self):
        fr_k = self.cleaned_data['fr_k']
        if fr_k == 0:
            fr_k = None
        elif fr_k < 0:
            self.fields['fr_k'].widget.attrs['class'] += ' is-invalid'
            raise forms.ValidationError("k can't be negative")
        return fr_k

    def clean_fa2_log_base(self):
        fa2_log_base = self.cleaned_data['fa2_log_base']
        if fa2_log_base < 0 or fa2_log_base == 1:
            self.fields['fa2_log_base'].widget.attrs['class'] += ' is-invalid'
            raise forms.ValidationError("Log base value can't be negative or 1")
        return fa2_log_base
