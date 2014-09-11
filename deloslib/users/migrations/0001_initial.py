# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('nro_usp', models.CharField(max_length=10, null=True, verbose_name='Numero USP', blank=True)),
                ('name', models.CharField(max_length=150, null=True, verbose_name='Nome', blank=True)),
                ('identification', models.CharField(unique=True, max_length=255, db_index=True)),
                ('email', models.EmailField(max_length=550, null=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('force_password_change', models.BooleanField(default=False)),
                ('uspdigital', models.BooleanField(default=False)),
                ('phone', models.CharField(max_length=100, null=True, verbose_name='Tel/Ramal', blank=True)),
                ('alternate_email', models.EmailField(max_length=550, null=True, blank=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Conta de Usu\xe1rio',
                'verbose_name_plural': 'Contas de Usu\xe1rios',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mail_from', models.EmailField(max_length=75, verbose_name='Email')),
                ('mail_name', models.CharField(max_length=255, verbose_name='Nome')),
                ('msg', models.TextField(verbose_name='Mensagem')),
                ('datetime', models.DateTimeField(auto_now=True, verbose_name='Data')),
                ('status', models.CharField(default=b'A', max_length=1, choices=[(b'A', b'Mensagem enviada, aguardando resposta'), (b'R', b'Mensagem respondida'), (b'P', b'Mensagem analisada e n\xc3\xa3o respondida')])),
                ('answer', models.TextField(null=True, verbose_name='Resposta', blank=True)),
                ('answer_person', models.ForeignKey(verbose_name='Respondido por', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Contato',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DelosApplication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(max_length=20, verbose_name='ID da aplica\xe7\xe3o')),
                ('name', models.CharField(max_length=200, verbose_name='Nome da aplica\xe7\xe3o')),
                ('is_public', models.BooleanField(default=False, verbose_name='App p\xfablica?')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DelosSite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('custom_menu', models.TextField(verbose_name='Menu customizado')),
                ('delos_apps', models.ManyToManyField(to='users.DelosApplication', null=True, blank=True)),
                ('site', models.ForeignKey(to='sites.Site', unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(max_length=1, verbose_name='Papel', choices=[(b'A', 'Administrador'), (b'C', 'Convidado'), (b'T', 'T\xe9cnico'), (b'O', 'Orientador'), (b'S', 'Secret\xe1ria')])),
                ('app', models.ForeignKey(verbose_name='Aplica\xe7\xe3o', to='users.DelosApplication')),
                ('person', models.ForeignKey(verbose_name='Pessoa', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Regra ou Permiss\xe3o',
                'verbose_name_plural': 'Regras e Permiss\xf5es',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Unidade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('abbreviation', models.CharField(max_length=10, verbose_name='Sigla')),
                ('name', models.CharField(max_length=150, verbose_name='Nome')),
                ('cnpj', models.CharField(max_length=20, null=True, verbose_name='CNPJ', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='role',
            name='unidade',
            field=models.ForeignKey(verbose_name='Unidade atual', to='users.Unidade'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='useraccount',
            name='last_app',
            field=models.ForeignKey(verbose_name='App atual', to='users.DelosApplication', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='useraccount',
            name='unidade',
            field=models.ForeignKey(verbose_name='Unidade atual', to='users.Unidade', null=True),
            preserve_default=True,
        ),
    ]
