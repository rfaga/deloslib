# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20141023_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='role',
            field=models.CharField(max_length=1, verbose_name='Papel', choices=[(b'A', 'Administrador'), (b'C', 'Convidado'), (b'T', 'T\xe9cnico'), (b'O', 'Orientador'), (b'S', 'Secret\xe1ria')]),
            preserve_default=True,
        ),
    ]
