#!/usr/bin/env python
# coding: UTF-8
from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, AbstractBaseUser, UserManager
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
    url = models.CharField(_(u'ID da aplicação'), max_length=20)
    name = models.CharField(_(u'Nome da aplicação'), max_length=200)
    is_public = models.BooleanField(_(u'App pública?'), default=False)
    
    def get_admins(self, unidade=None):
        q = Role.objects.filter(app=self, role='A')
        if unidade:
            q = Role.objects.filter(unidade=unidade)
        return [r.person for r in q]
    
    def __unicode__(self):
        return self.name

class DelosSite(models.Model):
    site = models.ForeignKey(Site, unique=True)
    custom_menu = models.TextField(_(u'Menu customizado'))
    delos_apps = models.ManyToManyField(DelosApplication, null=True, blank=True)
    
    def __unicode__(self):
        return self.site.name

class Unidade(models.Model):
    abbreviation = models.CharField(_(u'Sigla'), max_length=10)
    name = models.CharField(_(u'Nome'), max_length=150)
    cnpj = models.CharField(_(u'CNPJ'), max_length=20, blank=True, null=True)
    
    def __unicode__(self):
        return u'%s - %s' % (self.abbreviation, self.name)  







class UserAccount(AbstractBaseUser): #UserProfile
    unidade = models.ForeignKey(Unidade, verbose_name=_(u'Unidade atual'), null=True, blank=True)
    nro_usp = models.CharField(_(u'Numero USP'), max_length=10, blank=True, null=True)
    name = models.CharField(_(u'Nome'), max_length=150, blank=True, null=True)
    identification = models.CharField(unique=True, db_index=True, max_length=255)
    email = models.EmailField(null=True, max_length=550)
    is_staff = models.BooleanField(_(u'staff status'), default=False,
        help_text=_(u'Designates whether the user can log into this admin '
                    'site.'))
    last_app = models.ForeignKey(DelosApplication, verbose_name=_(u'App atual'), null=True, blank=True)
    
    force_password_change = models.BooleanField(default=False)
    
    uspdigital = models.BooleanField(default=False)
    
    phone = models.CharField(_(u'Tel/Ramal'), max_length=100, blank=True, null=True)
    alternate_email = models.EmailField(max_length=550, blank=True, null=True)
    
    USERNAME_FIELD = 'identification'
    
    objects = UserManager()
    
    @property
    def username(self):
        return self.identification
    
    @property
    def is_superuser(self):
        return self.is_staff
    
    class Meta:
        verbose_name = _(u"Conta de Usuário")
        verbose_name_plural = _(u"Contas de Usuários")
        ordering = ('name',)
        
    def __unicode__(self):
        return u'%s' % (self.name)
    
    def get_role(self, app_id, unidade=None):
        if not unidade:
            unidade = self.unidade
        try:
            return Role.objects.get(unidade=unidade, app__url=app_id, person=self)
        except:
            return None
    
    def get_email(self):
        return self.email
    
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
        
    def has_perm(self, perm, obj=None):
        return True
    def has_module_perms(self, app_label):
        return True
    def get_short_name(self):
        return self.name
    def get_username(self):
        return self.name

class Role(models.Model):
    person = models.ForeignKey(UserAccount, verbose_name=_(u'Pessoa'))
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
    answer_person = models.ForeignKey(UserAccount, verbose_name=_(u'Respondido por'), null=True, blank=True)
    
    class Meta:
        verbose_name = _(u"Contato")
