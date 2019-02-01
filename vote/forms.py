from django import forms

class Create_Poll(forms.Form):
    name = forms.CharField(label="Название опроса:",
                           max_length=100, required=True)
    variant_1 = forms.CharField(max_length=100, required=True)
    variant_2 = forms.CharField(max_length=100, required=True)
    variant_3 = forms.CharField(max_length=100, required=False)
    variant_4 = forms.CharField(max_length=100, required=False)
    variant_5 = forms.CharField(max_length=100, required=False)
    variant_6 = forms.CharField(max_length=100, required=False)
    variant_7 = forms.CharField(max_length=100, required=False)
    variant_8 = forms.CharField(max_length=100, required=False)
    variant_9 = forms.CharField(max_length=100, required=False)
    variant_10 = forms.CharField(max_length=100, required=False)



class User_Auth(forms.Form):
    username = forms.CharField(
        label="Имя пользователя", min_length=1, max_length=25, required=True)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput())


class Report_Form(forms.Form):
    poll_id = forms.IntegerField(
        label='ID опроса',
        min_value=1,
    )
    theme = forms.CharField(
        label='Тема жалобы',
        max_length=200,
    )
    text = forms.CharField(
        label='Жалоба',
        max_length=5000,
    )


class User_Email_Form(forms.Form):
    email = forms.EmailField(required=True)


class User_Edit_Form(forms.Form):
    password = forms.CharField(
        label="Ваш пароль", widget=forms.PasswordInput(), required=True)
    new_password = forms.CharField(
        label="Новый пароль", widget=forms.PasswordInput(), required=False)

    username = forms.CharField(
        label="Имя пользователя", min_length=1, max_length=25, required=False)
    email = forms.EmailField(
        label="Почта", min_length=1, max_length=25, required=False)
    first_name = forms.CharField(
        label="Имя", min_length=1, max_length=25, required=False)
    last_name = forms.CharField(
        label = "Фамилия", min_length = 1, max_length = 40, required = False)
