from django import forms

class Create_Pool(forms.Form):
    name = forms.CharField(label="Название опроса:",
                           max_length=100, required=True)
    variant_1 = forms.CharField(label="Первый вариант:",
                           max_length=100, required=True)
    variant_2 = forms.CharField(label="Второй вариант:",
                           max_length=100, required=False)
    variant_3 = forms.CharField(label="Третий вариант:",
                           max_length=100, required=False)
    variant_4 = forms.CharField(label="Четвёртый вариант:",
                           max_length=100, required=False)
    variant_5 = forms.CharField(label="Пятый вариант:",
                           max_length=100, required=False)
    variant_6 = forms.CharField(label="Шестой вариант:",
                           max_length=100, required=False)
    variant_7 = forms.CharField(label="Седьмой вариант:",
                           max_length=100, required=False)
    variant_8 = forms.CharField(label="Восьмой вариант:",
                           max_length=100, required=False)
    variant_9 = forms.CharField(label="Девятый вариант:",
                           max_length=100, required=False)
    variant_10 = forms.CharField(label="Десятый вариант:",
                           max_length=100, required=False)


class User_auth(forms.Form):
    username = forms.CharField(
        label="Имя пользователя:", min_length=1, max_length=25, required=True)
    password = forms.CharField(label="Пароль:", widget=forms.PasswordInput())
