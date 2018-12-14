from django import forms

class Create_Pool(forms.Form):
    name = forms.CharField(label="Название опроса", max_length=100, required=True)
    first_variant = forms.CharField(label="Первый вариант", max_length=100, required=True)
    second_variant = forms.CharField(label="Второй вариант", max_length=100, required=True)