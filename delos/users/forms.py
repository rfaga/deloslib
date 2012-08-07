#!/usr/bin/env python
# coding: UTF-8
from django import forms
from django.contrib.auth.forms import UserCreationForm
from captcha.fields import CaptchaField
### Forms
from django.contrib.auth.models import User
from form_utils.forms import BetterModelForm

class NewUserForm(BetterModelForm, UserCreationForm ):
    email = forms.EmailField(u'Email')
    captcha = CaptchaField(label=u'Digite o código')
    
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email = email)
            raise forms.ValidationError(u'Email já cadastrado!')
        except User.DoesNotExist:
            return email

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=True)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
