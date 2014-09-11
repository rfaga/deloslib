# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='last_app',
            field=models.ForeignKey(verbose_name='App atual', blank=True, to='users.DelosApplication', null=True),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='unidade',
            field=models.ForeignKey(verbose_name='Unidade atual', blank=True, to='users.Unidade', null=True),
        ),
    ]
