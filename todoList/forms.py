from django.forms import ModelForm
from todoList.models import TODO, lang
# from django.contrib.auth.forms import UserCreationForm
from django import forms
# from django.contrib.auth.models import User

class TODOForm(ModelForm):
    class Meta:
        model = TODO
        fields = ['title', 'status', 'description']


class TODOForm_Admin(ModelForm):
    class Meta:
        model = TODO
        fields = ['title', 'status', 'description', 'user']



class LangForm(ModelForm):
    class Meta:
        model = lang
        fields = ['language']

    # lang_choices = [
    #     ("en", "English"),
    #     ("de", "German"),
    # ]
    # language = forms.ChoiceField(choices=lang_choices, required=True)