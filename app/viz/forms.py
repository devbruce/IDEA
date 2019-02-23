from django import forms
import pandas as pd


class SnaUploadedFileCleanMixin(forms.Form):
    data = forms.FileField(
        required=True,
        label='Data',
        widget=forms.FileInput(
            attrs={
                'class': 'custom-file-input',
                'id': 'datafile',
                'aria-describedby': 'data-addon',
            }
        ),
        help_text='txt, csv files are supported. '
                  'One post must be entered per line(row).',
    )

    def clean_data(self):
        uploaded_data = self.cleaned_data['data']
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
            self.fields['data'].widget.attrs['class'] += ' is-invalid'
            raise forms.ValidationError("Uploaded File is not *.txt or *.csv")

    class Meta:
        abstract = True


class SnaForm(forms.Form):
    layouts = (
        ('fr', 'Fruchterman Reingold'),
        ('fa2', 'ForceAtlas2'),
    )
    network_size = (
        (35, 'Small (35)'),
        (60, 'Regular (60)'),
        (100, 'Large (100)'),
    )
    data = forms.CharField(
        required=False,
        label='Data Input Box',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control data-box',
                'placeholder': "Put your data here. If you try to visualize with blank,"
                               "sample data is automatically entered.",
            }
        ),
        help_text='One post must be entered per line.'
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
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb-1'
            }
        ),
    )
    stopwords = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'ex) text,data,visualizer'
            }
        ),
        help_text='Type the words you want to exclude from the results. '
                  '(If there are several, separate them by comma)',
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
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    layout = forms.ChoiceField(required=True, choices=layouts, initial='fr',)
    fr_k = forms.IntegerField(
        required=True,
        label='Variable k',
        initial=0,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb-1'
            }
        ),
        help_text='As the value increases, the distance of the node increases. '
                  'Default 0 equals None',
    )
    fa2_square = forms.IntegerField(required=True, label='Variable Square', initial=2,)
    fa2_log_base = forms.IntegerField(
        required=True,
        label='Variable log(base)',
        initial=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb-1'
            }
        ),
    )

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
        if fr_k < 0:
            self.fields['fr_k'].widget.attrs['class'] += ' is-invalid'
            raise forms.ValidationError("k can't be negative")
        return fr_k

    def clean_fa2_log_base(self):
        fa2_log_base = self.cleaned_data['fa2_log_base']
        if fa2_log_base < 0 or fa2_log_base == 1:
            self.fields['fa2_log_base'].widget.attrs['class'] += ' is-invalid'
            raise forms.ValidationError("Log base value can't be negative or 1")
        return fa2_log_base


class SnaInteractiveForm(SnaForm):
    theme_list = (
        ('default', 'Default'),
        ('light', 'Light'),
        ('dark', 'Dark'),
    )
    theme = forms.ChoiceField(required=True, choices=theme_list, initial='default',)


class SnaFileForm(SnaUploadedFileCleanMixin, SnaForm):
    pass


class SnaInteractiveFileForm(SnaUploadedFileCleanMixin, SnaInteractiveForm):
    pass


class WcForm(forms.Form):
    bg_colors = (
        ('white', 'White'),
        ('black', 'Black'),
        ('gray', 'Gray'),
    )
    data = forms.CharField(
        required=False,
        label='Data Input Box',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control data-box mb-3',
                'placeholder': 'Put your data here. If you try to visualize with blank,'
                               'sample data is automatically entered.'
            }
        )
    )
    stopwords = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'ex) text,data,visualizer'
            }
        ),
        help_text='Type the words you want to exclude from the results. '
                  '(If there are several, separate them by comma)',
    )
    max_word_size = forms.IntegerField(
        required=True,
        label='Max Word Size',
        initial=100,
        widget=forms.TextInput(attrs={'class': 'form-control mb-1'}),
        help_text='Specify the most frequent word size.'
    )
    bg_color = forms.ChoiceField(
        required=True,
        label='Background Color',
        choices=bg_colors,
        initial='white',
    )
    font = forms.FileField(
        required=False,
        widget=forms.FileInput(
            attrs={
                'class': 'custom-file-input',
                'id': 'fontfile',
                'aria-describedby': 'fontfile-addon',
            }
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
        help_text='Brings the color of the mask intact. Default : OFF',
    )

    def clean_font(self):
        font_file = self.cleaned_data['font']
        if not font_file:
            return None
        file_extension = str(font_file)[-3:]
        if file_extension not in ('ttf', 'otf'):
            self.fields['font'].widget.attrs['class'] += ' is-invalid'
            raise forms.ValidationError('Uploaded File is not font file. (This file has not font extensions.)')
        return font_file

    def clean_max_word_size(self):
        max_word_size = self.cleaned_data['max_word_size']
        if max_word_size < 0:
            self.fields['max_word_size'].widget.attrs['class'] += ' is-invalid'
            raise forms.ValidationError("Max Word Size can't be negative")
        return max_word_size


class WcFileForm(WcForm):
    data = forms.FileField(
        required=True,
        label='Data',
        widget=forms.FileInput(
            attrs={
                'class': 'custom-file-input',
                'id': 'datafile',
                'aria-describedby': 'data-addon',
            }
        ),
        help_text='txt, csv files are supported.',
    )

    def clean_data(self):
        uploaded_data = self.cleaned_data['data']
        if uploaded_data.content_type == 'text/plain':
            return uploaded_data.read().decode()
        elif uploaded_data.content_type == 'text/csv':
            data_raw = pd.read_csv(uploaded_data, encoding='CP949', header=None)
            data = ''
            for post in data_raw[0]:
                data += post
            return data
        else:
            self.fields['data'].widget.attrs['class'] += ' is-invalid'
            raise forms.ValidationError("Uploaded File is not *.txt or *.csv")
