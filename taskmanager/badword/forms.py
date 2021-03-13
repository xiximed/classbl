from .models import Task
from django.forms import ModelForm, TextInput


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ["title", "task"]
        widgets = {"title": TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите Название'
        }),
            "task": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите Текст'
            })
        }


class TextsFormSecond(ModelForm):
    class Meta:
        model = Task
        fields = ["task"]
        widgets = {
            "task": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите текст на русском языке'

            })
        }

class FiltCat(ModelForm):
    class Meta:

        model = Task
        fields = ['title', 'task']