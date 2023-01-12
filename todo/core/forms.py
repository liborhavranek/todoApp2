from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    date_planned_completion = forms.DateTimeField(label='Time in future', widget=forms.TextInput(attrs={'id': 'time_in_future', 'type':'datetime-local', 'class':'form-control'}))
    class Meta:
        model = Task
        fields = ['title', 'text', 'date_planned_completion', 'complete']
        



