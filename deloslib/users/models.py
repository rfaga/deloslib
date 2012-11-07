#!/usr/bin/env python
# coding: UTF-8
from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

#from django.db.models import signals

RELATIONS = (
    ('A', _(u'Administrador')),
    ('C', _(u'Convidado')),
    ('O', _(u'Operador / Técnico')),
    ('D', _(u'Docente')),
    
)

CONTACT_STATUS = (
    ('A', 'Mensagem enviada, aguardando resposta'),
    ('R', 'Mensagem respondida'),
    ('P', 'Mensagem analisada e não respondida'),
)

class DelosApplication(models.Model):
    url = models.CharField(_('ID da aplicação'), max_length=20)
    name = models.CharField(_('Nome da aplicação'), max_length=200)
    is_public = models.BooleanField(_('App pública?'), default=False)
    
    def get_admins(self, unidade=None):
        q = Role.objects.filter(app=self, role='A')
        if unidade:
            q = Role.objects.filter(unidade=unidade)
        return [r.person for r in q]
    
    def __unicode__(self):
        return self.name

class Unidade(models.Model):
    abbreviation = models.CharField(_(u'Sigla'), max_length=10)
    name = models.CharField(_(u'Nome'), max_length=150)
    cnpj = models.CharField(_(u'CNPJ'), max_length=20, blank=True, null=True)
    
    def __unicode__(self):
        return u'%s - %s' % (self.abbreviation, self.name)  


class Person(models.Model): #UserProfile
    unidade = models.ForeignKey(Unidade, verbose_name=_(u'Unidade atual'), null=True)
    nro_usp = models.CharField(_(u'Numero USP'), max_length=10, blank=True, null=True)
    name = models.CharField(_(u'Nome'), max_length=150, blank=True, null=True)
    user = models.ForeignKey(User, unique=True, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    
    
    class Meta:
        verbose_name = _(u"Pessoa")
        ordering = ('name',)
        
    def __unicode__(self):
        return u'%s' % (self.name)
    
    def get_role(self, app_id):
        try:
            return Role.objects.get(unidade=self.unidade, app__url=app_id, person=self)
        except:
            return None
    
    def get_email(self):
        if self.email:
            return self.email
        elif self.user:
            return self.user.email
        else:
            raise Exception('No email found')
    
    def get_possible_apps(self):
        query = Role.objects.filter(unidade=self.unidade, person=self).values_list('app__url', 'app__name').distinct()
        return list([{'url': x[0], 'name': x[1]} for x in query]) + list(DelosApplication.objects.filter(is_public=True).values('url', 'name'))

class Role(models.Model):
    person = models.ForeignKey(Person)
    app = models.ForeignKey(DelosApplication)
    unidade = models.ForeignKey(Unidade, verbose_name=_(u'Unidade atual'))
    role = models.CharField(max_length=1, choices=RELATIONS)
    
    class Meta:
        verbose_name = _(u"Regra ou Permissão")
        verbose_name_plural = _(u"Regras e Permissões")
    
    def is_admin(self):
        return self.role == 'A'

    def __unicode__(self):
        return u'%s (%s) - %s' % (self.get_role_display(), self.app_id, self.person)


class Contact(models.Model):
    mail_from = models.EmailField(_(u'Email'))
    mail_name = models.CharField(_(u'Nome'), max_length=255)
    msg = models.TextField(_(u'Mensagem'))
    datetime = models.DateTimeField(_(u'Data'), auto_now=True)
    status = models.CharField(max_length=1, choices=CONTACT_STATUS, default='A')
    answer = models.TextField(_(u'Resposta'), blank=True, null=True)
    answer_person = models.ForeignKey(Person, verbose_name=_(u'Respondido por'), null=True, blank=True)
    
    class Meta:
        verbose_name = _(u"Contato")
