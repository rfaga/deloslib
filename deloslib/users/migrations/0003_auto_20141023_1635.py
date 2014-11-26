# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20140910_1700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='role',
            field=models.CharField(max_length=1, verbose_name='Papel', choices=[(b'A', 'Administrador'), (b'O', 'Orientador'), (b'R', 'Representante de Grupo'), (b'C', 'Coordenador'), (b'S', 'Secretaria')]),
            #preserve_default=True,
        ),
    ]
