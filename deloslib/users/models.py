#!/usr/bin/env python
# coding: UTF-8
from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.conf import settings

#from django.db.models import signals


RELATIONS = (
    ('A', _(u'Administrador')),
    ('C', _(u'Convidado')),
    ('T', _(u'Técnico')),
    ('O', _(u'Orientador')),
    ('S', _(u'Secretária')),
)

if getattr(settings, 'RELATIONS', None):
    RELATIONS = settings.RELATIONS

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

class DelosSite(models.Model):
    site = models.ForeignKey(Site, unique=True)
    custom_menu = models.TextField(_('Menu customizado'))
    delos_apps = models.ManyToManyField(DelosApplication, null=True, blank=True)
    
    def __unicode__(self):
        return self.site.name

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
        query = DelosApplication.objects.filter(
                            models.Q(role__person=self, role__unidade=self.unidade) |
                            models.Q(is_public=True)).distinct().values('url', 'name')
        return list(query)

    def get_unities(self):
        query = Role.objects.filter(person=self).values_list('unidade__abbreviation', 'unidade__name').distinct()
        if len(query) > 1:
            return query
        return None
        

class Role(models.Model):
    person = models.ForeignKey(Person, verbose_name=_(u'Pessoa'))
    app = models.ForeignKey(DelosApplication, verbose_name=_(u'Aplicação'))
    unidade = models.ForeignKey(Unidade, verbose_name=_(u'Unidade atual'))
    role = models.CharField(max_length=1, choices=RELATIONS, verbose_name=_(u'Papel'))
    
    class Meta:
        verbose_name = _(u"Regra ou Permissão")
        verbose_name_plural = _(u"Regras e Permissões")
    
    def is_admin(self):
        return self.role == 'A'
    
    def is_tech(self):
        return self.role == 'T'

    def is_supervisor(self):
        return self.role == 'O'

    def is_leader(self):
        return self.role == 'R'

    def is_secretary(self):
        return self.role == 'S'
        
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
