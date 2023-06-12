import uuid

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

from django import forms


class CustomUserCreationForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name","organization")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.organization = self.cleaned_data['organization']
        user.set_password(str(uuid.uuid4()))  # set password to a random UUID
        if commit:
            user.save()
        return user