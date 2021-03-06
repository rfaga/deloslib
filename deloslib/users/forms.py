#!/usr/bin/env python
# coding: UTF-8
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm,\
    AuthenticationForm
from captcha.fields import CaptchaField
from django.utils.translation import ugettext as _
### Forms
from models import UserAccount
from django.conf import settings
from deloslib.users import send_mail
from django.core.mail.message import EmailMessage
from django.contrib.auth import get_user_model

class NewUserForm(forms.ModelForm):
    name = forms.CharField(label=_(u'Nome Completo'), max_length=255, min_length=4, required=True)
    nro_usp = forms.CharField(label=_(u'Número USP'), max_length=8, min_length=0, required=False)
    email = forms.EmailField(label=u'Email', required=True)
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label=_("Password confirmation"), widget=forms.PasswordInput,
        help_text = _("Enter the same password as above, for verification."), required=True)

    captcha = CaptchaField(label=_(u'Digite o código'), required=True)

    class Meta:
        fields = ('email', 'name', 'nro_usp')
        model = UserAccount

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            UserAccount.objects.get(email = email)
            raise forms.ValidationError(_(u'Email já cadastrado!'))
        except UserAccount.DoesNotExist:
            return email

    def clean_nro_usp(self):
        nro_usp = self.cleaned_data['nro_usp']
        if nro_usp.strip():
            try:
                UserAccount.objects.get(nro_usp = nro_usp)
                raise forms.ValidationError(_(u'Número USP já cadastrado!'))
            except UserAccount.DoesNotExist:
                try:
                    UserAccount.objects.get(identification = nro_usp)
                    raise forms.ValidationError(_(u'Número USP já cadastrado!'))
                except UserAccount.DoesNotExist:
                    return nro_usp
        else:
            return ''

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
#        user.is_active = True
        nro_usp = user.nro_usp
        if nro_usp:
            user.identification = nro_usp
        else:
            user.identification = user.email
        user.save()
        return user


class ChangePasswordForm(forms.ModelForm):
    next = forms.CharField(widget=forms.HiddenInput(), required=False)
    password_old = forms.CharField(label=_("Senha anterior"), widget=forms.PasswordInput, required=True)
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label=_("Password confirmation"), widget=forms.PasswordInput,
        help_text = _("Enter the same password as above, for verification."), required=True)

    class Meta:
        fields = tuple()
        model = UserAccount

    def clean_next(self):
        next = self.cleaned_data.get("next", "")
        if not next:
            return "/"
        else:
            return next

    def clean_password_old(self):
        if not getattr(self, 'instance', None) or not self.instance.is_authenticated():
            raise forms.ValidationError(_(u"Só é possível editar um usuário"))
        password = self.cleaned_data.get("password_old", "")
        if self.instance.check_password(password):
            return True
        else:
            raise forms.ValidationError(_(u"A senha anterior está incorreta."))

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

    def save(self, commit=True):
        user = super(ChangePasswordForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.force_password_change = False
        user.save()
        return user


class CustomizedAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label=_("Username"), max_length=255)


class ContactForm(forms.Form):
    name = forms.CharField(label="Nome", required=True)
    email = forms.EmailField(label="Email", required=True)
    msg = forms.CharField(label="Mensagem", required=True,
        widget=forms.Textarea(attrs={'cols':'100', 'rows':'10'}))

    def send_mail(self):
        name, email, msg = self.data['name'], self.data['email'], self.data['msg']
        msg = ("Mensagem de '%s (%s)':\n----------------\n"% (name, email)) + msg
        contacts = getattr(settings, 'CONTACTS', settings.ADMINS)
        to = [x[1] for x in contacts]
        email = EmailMessage(subject="Delos - Contato pelo site", body=msg, to=to, headers={'reply-to': email})
        email.encoding = 'utf-8'
        email.send(fail_silently=True)
