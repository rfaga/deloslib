#!/usr/bin/env python
# coding: UTF-8
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from captcha.fields import CaptchaField
from django.utils.translation import ugettext as _
### Forms
from django.contrib.auth.models import User
from models import Person
from django.conf import settings

class NewUserForm(forms.ModelForm):
    name = forms.CharField(label=_(u'Nome Completo'), max_length=255, min_length=4, required=True)
    nro_usp = forms.CharField(label=_(u'Número USP'), max_length=8, min_length=0, required=False)
    email = forms.EmailField(u'Email', required=True)
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label=_("Password confirmation"), widget=forms.PasswordInput,
        help_text = _("Enter the same password as above, for verification."), required=True)
    
    captcha = CaptchaField(label=_(u'Digite o código'), required=True)
    
    class Meta:
        fields = ('email',)
        model = User
    
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email = email)
            raise forms.ValidationError(_(u'Email já cadastrado!'))
        except User.DoesNotExist:
            return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(_("The two password fields didn't match."))
        return password2
    
    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["name"]
#        user.is_active = True
        nro_usp = self.cleaned_data["nro_usp"]
        if nro_usp:
            user.username = nro_usp
        else:
            user.username = user.email[:30]
        if commit:
            user.save()
            Person.objects.create(
                name=self.cleaned_data["name"],
                nro_usp = nro_usp,
                user=user,
                unidade=None)
        return user

