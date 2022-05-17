from django import forms
from django.contrib.auth.models import User


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": 'Username', "name": 'username',
                   "class": "auth-form__input"}),
        label='',
        required=True
    )

    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={'placeholder': 'Email', "name": 'email',
                   "class": "auth-form__input"}),
        label='',
        required=True
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Password', "name": 'password',
                   "class": "auth-form__input"}),
        label='',
        required=True
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Confirm Password', "name": 'passowrd2',
                   "class": "auth-form__input"}),
        label='',
        required=True
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email already used.')
        return email
