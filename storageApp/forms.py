from django import forms
from .models import InputSignal

class InputSignalForm(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))

    input_file = forms.FileField(widget=forms.FileInput(
        attrs={
            'class': 'form-control-file'
        }
    ))

    adnotations = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control'
        }))

    amplitude_unit = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))

    sample_rate = forms.FloatField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'type': 'number',
            'step': 'any',
        }
    ))

    class Meta:
        model = InputSignal
        exclude = ["author", "add_date", "last_edit_date", "results_file"]
