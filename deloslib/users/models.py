#!/usr/bin/env python
# coding: UTF-8
from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

class Unidade(models.Model):
    abbreviation = models.CharField(_(u'Sigla'), max_length=10)
    name = models.CharField(_(u'Nome'), max_length=150)
    cnpj = models.CharField(_(u'CNPJ'), max_length=20, blank=True, null=True)
    
    def __unicode__(self):
        return u'%s - %s' % (self.abbreviation, self.name)  


class Person(models.Model): #UserProfile
    class Meta:
        ordering = ('name',)
    unidade = models.ForeignKey(Unidade, verbose_name=_(u'Unidade atual'))
    nro_usp = models.CharField(_(u'Numero USP'), max_length=10, blank=True, null=True)
    name = models.CharField(_(u'Nome'), max_length=150, blank=True, null=True)
    user = models.ForeignKey(User, unique=True, blank=True, null=True)
    class Meta:
        verbose_name = _(u"Pessoa")
        
        
    def __unicode__(self):
        return u'%s' % (self.name)
    
    def get_role(self, app_id):
        try:
            return Role.objects.get(unidade=self.unidade, app_id=app_id, person=self)
        except:
            return Role(role='')


RELATIONS = (
    ('A', _(u'Administrador')),
    ('C', _(u'Convidado')),
    ('O', _(u'Operador / Técnico')),
    ('D', _(u'Docente')),
    
)
APP_IDS = (
    ('users', _(u'Módulo de Usuários')),
    ('news', _(u'Módulo de Notícias')),
    ('nfe', _(u'Módulo de Notas Fiscais')),
    ('gradprogram', _(u'Módulo de Inscrição na Pós')),
    ('conference', _(u'Módulo de Conferências')),
    ('memo', _(u'Módulo de Memorandos')),
)
class Role(models.Model):
    person = models.ForeignKey(Person)
    app_id = models.CharField(max_length=30, verbose_name=_(u'ID da aplicação'), choices=APP_IDS)
    unidade = models.ForeignKey(Unidade, verbose_name=_(u'Unidade atual'))
    role = models.CharField(max_length=1, choices=RELATIONS)
    
    class Meta:
        verbose_name = _(u"Regra ou Permissão")
        verbose_name_plural = _(u"Regras e Permissões")
    
    def is_admin(self):
        return self.role == 'A'

    def __unicode__(self):
        return u'%s (%s) - %s' % (self.get_role_display(), self.app_id, self.person)
