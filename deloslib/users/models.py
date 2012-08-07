#!/usr/bin/env python
# coding: UTF-8
from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

class Unidade(models.Model):
    abbreviation = models.CharField(u'Sigla', max_length=10)
    name = models.CharField(u'Nome', max_length=150)
    cnpj = models.CharField(u'CNPJ', max_length=20, blank=True, null=True)
    
    def __unicode__(self):
        return u'%s - %s' % (self.abbreviation, self.name)  


class Person(models.Model): #UserProfile
    class Meta:
        ordering = ('name',)
    unidade = models.ForeignKey(Unidade, verbose_name=u'Unidade atual')
    nro_usp = models.CharField(u'Numero USP', max_length=10, blank=True, null=True)
    name = models.CharField(u'Nome', max_length=150, blank=True, null=True)
    user = models.ForeignKey(User, unique=True, blank=True, null=True)
    
    def __unicode__(self):
        return u'%s' % (self.name)
    
    def get_role(self, app_id):
        try:
            return Role.objects.get(unidade=self.unidade, app_id=app_id, user=self.user)
        except:
            return Role(role='')


RELATIONS = (
    ('', 'None'),
    ('A', 'Administrador'),
    ('C', 'Convidado'),
    ('O', 'Operador'),
)
class Role(models.Model):
    user = models.ForeignKey(User)
    app_id = models.CharField(max_length=30, verbose_name=u'ID da aplicação')
    unidade = models.ForeignKey(Unidade, verbose_name=u'Unidade atual')
    role = models.CharField(max_length=1, choices=RELATIONS)
    
    def is_admin(self):
        return self.role == 'A'

    def __unicode__(self):
        return u'%s (%s) - %s' % (self.role.get_display(), self.app_id, self.user.name)   

#class Group(models.Model):
#    unidade = models.ForeignKey(u'Unidade', verbose_name=u'Unidade')
#    name = models.CharField(u'Nome', max_length=150, blank=True,null=True)
#    app = models.CharField(max_length=20, verbose_name=u'Aplicação (nome Python)', null=True)
#    locked = models.BooleanField(u'Estático', help_text=u'Bloqueia o grupo de edições pelos administradores locais', default=False)
#    official = models.BooleanField(u'Oficial', help_text=u'Trata-se de um grupo oficial, reconhecido pelo organograma da unidade.', default=False)
#    def __unicode__(self):
#        return u'%s' % (self.name)
#    def get_children(self, type=None):
#        relations = GroupRelation.objects.filter(parent = self)
#        if type:
#            relations.filter(type = type)
#        groups = list(relations.values_list('group', flat=True).distinct())
#        users = list(relations.values_list('user', flat=True).distinct())
#        try:
#            groups.remove(None)
#        except:
#            pass
#        try:
#            users.remove(None)
#        except:
#            pass
#        for relation in relations:
#            if relation.group:
#                (new_groups, new_users) = relation.group.get_children(type)
#                groups += new_groups
#                users += new_users
#        return groups, users
#
#RELATIONS = (
#    ('A', 'Administrador'),
#    ('C', 'Convidado'),
#    ('O', 'Operador'),
#    ('E', 'Estrutural'),
#)
#
#class GroupRelation(models.Model):
#    parent = models.ForeignKey(Group, verbose_name=u'Grupo', related_name='parent_group')
#    type = models.CharField(choices = RELATIONS, max_length=1)
#    group = models.ForeignKey(Group, verbose_name=u'Grupo participante', null=True)
#    user = models.ForeignKey(Person, verbose_name=u'Usuário participante', null=True)
#    expiry_date = models.DateField(verbose_name=u'Data de expiração', null=True)
#    preferable = models.BooleanField(verbose_name=u'Preferencial')
#    #class Meta:
#    #    unique_together = (('parent', 'type' ))
#
#def get_app_members(app_name, unidade):
#    main_group = Group.objects.filter(app = app_name, unidade = unidade)
    

#group = Group()
#grupos = GroupRelation.objects.groups( parent = group)