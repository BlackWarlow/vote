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
    type = forms.CharField(
        label='Тема жалобы',
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    text = forms.CharField(
        label='Жалоба',
        max_length=5000,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'style': 'height:500px'
            }
        )
    )


class User_Register(forms.Form):