from django import forms
from .models import ModelAutoSNA, ModelAutoWC, ModelSNA, ModelWC

class FormAutoSNA(forms.ModelForm):

    class Meta:
        model = ModelAutoSNA
        fields = ('edge_remove_threshold', 'node_num', 'page_range', 'stop_words', 
        'remove_isolated_node', 'layout', 'fr_k', 'fr_iter', 'fa2_1', 'fa2_2', 'fa2_iter', 'keyword',)

class FormAutoWC(forms.ModelForm):

    class Meta:
        model = ModelAutoWC
        fields = ('page_range', 'stop_words', 'keyword',)

class FormSNA(forms.ModelForm):

    class Meta:
        model = ModelSNA
        fields = ('edge_remove_threshold', 'node_num', 'stop_words',
        'remove_isolated_node', 'layout', 'fr_k', 'fr_iter', 'fa2_1', 'fa2_2', 'fa2_iter', 'text_input',)

class FormWC(forms.ModelForm):

    class Meta:
        model = ModelWC
        fields = ('stop_words', 'text_input',)