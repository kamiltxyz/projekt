from django import forms
from projekt_core.models import Project


# Projects
class NewProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title']


class TerminalForm(forms.Form):
    command = forms.CharField()
