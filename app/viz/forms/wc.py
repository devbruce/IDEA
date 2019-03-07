from django import forms
from .base import VizBaseForm
import pandas as pd


class WcForm(VizBaseForm):
    bg_colors = (
        ('white', 'White'),
        ('black', 'Black'),
        ('gray', 'Gray'),
    )
    max_word_size = forms.IntegerField(
        required=True,
        label='Max Word Size',
        initial=100,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control'
            },
        ),
        help_text='Specify the most frequent word size.',
    )
    bg_color = forms.ChoiceField(
        required=True,
        label='Background Color',
        choices=bg_colors,
        initial='white',
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            },
        ),
    )
    font = forms.FileField(
        required=False,
        widget=forms.FileInput(
            attrs={
                'class': 'custom-file-input',
                'id': 'fontfile',
                'aria-describedby': 'fontfile-addon',
            },
        ),
        help_text='Default Font is DOSGothic',)
    mask = forms.ImageField(
        required=False,
        label='Mask Image',
        help_text='Shape of Wordcloud. Default mask is black circle',
    )
    mask_coloring = forms.BooleanField(
        required=False,
        label='Mask Coloring',
        initial=False,
        help_text='Brings the color of the mask intact. (Default : OFF)',
    )

    def clean_data_file(self):
        uploaded_data = self.cleaned_data['data_file']
        if uploaded_data:
            if uploaded_data.content_type == 'text/plain':
                return uploaded_data.read().decode()
            elif uploaded_data.content_type == 'text/csv':
                data_raw = pd.read_csv(uploaded_data, encoding='CP949', header=None)
                data = ''
                for post in data_raw[0]:
                    data += post
                return data
            else:
                self.fields['data_file'].widget.attrs['class'] += ' is-invalid'
                raise forms.ValidationError("Uploaded File is not *.txt or *.csv")
        else:
            return None

    def clean_max_word_size(self):
        max_word_size = self.cleaned_data['max_word_size']
        if max_word_size < 0:
            self.fields['max_word_size'].widget.attrs['class'] += ' is-invalid'
            raise forms.ValidationError("Max Word Size can't be negative")
        return max_word_size

    def clean_font(self):
        font_file = self.cleaned_data['font']
        if not font_file:
            return None
        file_extension = str(font_file)[-3:]
        if file_extension not in ('ttf', 'otf'):
            self.fields['font'].widget.attrs['class'] += ' is-invalid'
            raise forms.ValidationError('Uploaded File is not font file. (This file has not font extensions.)')
        return font_file
