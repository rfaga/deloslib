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
APP_IDS = (
    ('users', _(u'Usuários')),
    ('news', _(u'Notícias')),
    ('nfe', _(u'Notas Fiscais')),
    ('gradprogram', _(u'Inscrição na Pós')),
    ('conference', _(u'Conferências')),
    ('memo', _(u'Memorandos')),
)


class DelosApplication(models.Model):
    url = models.CharField(_('ID da aplicação'), max_length=20)
    name = models.CharField(_('Nome da aplicação'), max_length=200)
    is_public = models.BooleanField(_('App pública?'), default=False)
    
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

class UserActivation(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    token = models.CharField(_(u'Token'), max_length=20)
    user = models.ForeignKey(User, unique=True)