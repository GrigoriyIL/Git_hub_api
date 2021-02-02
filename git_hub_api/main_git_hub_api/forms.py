from django import forms
from .models import Repository
import re
from django.core.exceptions import ValidationError


class RepositoryForm(forms.Form):
    repository_url = forms.URLField(label='Сылка на репозиторий', 
    widget=forms.TextInput(attrs={"class": "form-control"}))

    # def clean_repository_url(self):
    #     repository_url = self.cleaned_data['repository_url']
    #     if re.match(r'https://github.com/', repository_url):
    #         raise ValidationError('Не валидная ссылка')
    #     return repository_url 