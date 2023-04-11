""" Describes SignInForm SignUpForm form """

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()


class SignInForm(forms.Form):
    """This class describes login form"""

    username = forms.CharField(label='Username', required=True,
                               max_length=32, widget=forms.TextInput(attrs={
        "class": "form-control",
        "id": "username",
        "placeholder": "Username"
    }))
    password = forms.CharField(label='Password', required=True, widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "id": "password",
        "placeholder": "Password"
    }))
    user = None

    def clean(self):
        """This method to provide custom model validation and to modify attributes. """

        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if username and password:
            self.user = authenticate(username=username, password=password)
            if self.user is None:
                raise forms.ValidationError('Please, check the form ')


class SignUpForm(forms.Form):
    """This class describes register form"""

    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={
        "class": "form-control",
        "id": "username",
        "placeholder": "Username"
    }))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={
        "class": "form-control",
        "id": "email",
        "placeholder": "Email"

    }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "id": "password",
        "placeholder": "Password"
    }))
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "id": "confirmPassword",
        "placeholder": "Password"
    }))

    def clean_username(self):
        """This method to provide custom model validation and to modify attributes. """

        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
            raise ValidationError("This Username already exists.")
        except User.DoesNotExist:
            return username

    def clean_email(self):
        """This method to provide custom model validation and to modify attributes. """

        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
            raise ValidationError("This email already exists.")
        except User.DoesNotExist:
            return email

    def clean(self):
        """This method to provide custom model validation and to modify attributes. """

        password = self.cleaned_data["password"]
        confirm_password = self.cleaned_data["confirm_password"]
        if password != confirm_password:
            # raise ValidationError("password do not match")
            self.add_error("password", "Passwords do not match, please check")

    def save(self):
        """The method which is executed to save an instance"""

        del self.cleaned_data["confirm_password"]
        User.objects.create_user(**self.cleaned_data)
