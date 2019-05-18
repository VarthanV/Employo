from django.forms import forms
class ResumeForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max.5 megabytes'
    )