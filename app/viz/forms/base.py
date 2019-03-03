from django import forms
from django.conf import settings
import os


class VizBaseForm(forms.Form):
    data = forms.CharField(
        required=False,
        label='Data Input',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control data-box',
                'placeholder': 'Put your data here.',
            }
        ),
    )
    data_file = forms.FileField(
        required=False,
        label='Data File Input',
        widget=forms.FileInput(
            attrs={
                'class': 'custom-file-input',
                'id': 'datafile',
                'aria-describedby': 'data-addon',
            }
        ),
        help_text='txt, csv files are supported.',
    )
    stopwords = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'ex) Word1,Word2,Word3',
            }
        ),
        help_text='Type the words you want to exclude from the results. '
                  '(If there are several, separate them by comma)',
    )
    word_len_min = forms.IntegerField(
        required=True,
        label='Minimum Word Length',
        initial=2,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control mb-1',
            }
        )
    )

    def clean_stopwords(self):
        stopwords = self.cleaned_data['stopwords']
        if not stopwords:
            return None
        else:
            return stopwords

    def clean_word_len_min(self):
        word_len_min = self.cleaned_data['word_len_min']
        if word_len_min < 1:
            self.fields['word_len_min'].widget.attrs['class'] += ' is-invalid'
            raise forms.ValidationError("Minimum Word Length can't be less than 1")
        return word_len_min

    def clean(self):
        data = self.cleaned_data.pop('data')
        data_file = self.cleaned_data.pop('data_file') if 'data_file' in self.cleaned_data else None
        if not data and not data_file:  # Both are empty
            try:
                self.cleaned_data['data'] = open(os.path.join(settings.ROOT_DIR, 'sample_data.txt'), 'rt').read()
            except FileNotFoundError:
                raise forms.ValidationError('Sample data does not exists')
        elif data and data_file:  # Both are entered
            if type(data_file) == list:  # if data_file is csv
                self.cleaned_data['data'] = data.split('\n') + data_file
            else:
                self.cleaned_data['data'] = data + data_file
        else:
            self.cleaned_data['data'] = data or data_file
        return self.cleaned_data
