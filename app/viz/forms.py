from django import forms


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
        widget=forms.Textarea(), required=False,
        help_text='One post must be entered per line.'
    )
    node_num = forms.ChoiceField(choices=network_size, initial=35, help_text='Number of nodes', required=True)
    edge_remove_threshold = forms.IntegerField(initial=0, required=True)
    stopwords = forms.CharField(help_text='Type the words you want to exclude from the results. '
                                          '(If there are several, separate them by comma)',
                                required=False)
    remove_isolated_node = forms.BooleanField(initial=True, help_text='Default : ON', required=False)
    layout = forms.ChoiceField(choices=layouts, initial='fr', required=True)
    iterations = forms.IntegerField(initial=50, required=True)
    fr_k = forms.IntegerField(initial=0, help_text='As the value increases, the distance of the node increases. '
                                                   'Default 0 equals None',
                              required=True)
    fa2_square = forms.IntegerField(initial=2, required=True)
    fa2_log_base = forms.IntegerField(initial=100, required=True)


class SnaFileForm(SnaForm):
    data = forms.FileField(help_text='txt, csv files are supported. '
                                     'One post must be entered per line(row).',
                           required=True)


class SnaInteractiveForm(SnaForm):
    theme_list = (
        ('default', 'Default'),
        ('light', 'Light'),
        ('dark', 'Dark'),
    )
    theme = forms.ChoiceField(choices=theme_list, initial='default', required=True)


class SnaInteractiveFileForm(SnaInteractiveForm):
    data = forms.FileField(help_text='txt, csv files are supported. '
                                     'One post must be entered per line(row).',
                           required=True)


class WcForm(forms.Form):
    bg_colors = (
        ('white', 'White'),
        ('black', 'Black'),
        ('gray', 'Gray'),
    )
    data = forms.CharField(widget=forms.Textarea(), required=False)
    stopwords = forms.CharField(help_text='Type the words you want to exclude from the results. '
                                          '(If there are several, separate them by comma)',
                                required=False)
    max_word_size = forms.IntegerField(initial=100, help_text='Specify the most frequent word size.',
                                       required=True)
    bg_color = forms.ChoiceField(choices=bg_colors, initial='white', required=True)
    mask = forms.ImageField(help_text='Shape of wordcloud. default mask is black circle',
                            required=False)
    mask_coloring = forms.BooleanField(initial=False,
                                       help_text='Brings the color of the mask intact. Default : OFF',
                                       required=False)
    font = forms.FileField(help_text='Default Font is DOSGothic',
                           required=False)


class WcFileForm(WcForm):
    data = forms.FileField(help_text='txt, csv files are supported.',
                           required=True)
