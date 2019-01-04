from django import forms

class Create_Pool(forms.Form):
    name = forms.CharField(label="Название опроса", max_length=100, required=True)
    first_variant = forms.CharField(label="Первый вариант", max_length=100, required=True)
    second_variant = forms.CharField(
        label="Второй вариант", max_length=100, required=True)

class User_auth(forms.Form):
    username = forms.CharField(
        label="Имя пользователя", min_length=3, max_length=25, required=True)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput())