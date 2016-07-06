# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-19 16:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cs_questions', '0003_auto_20160619_1206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answerkeyitem',
            name='iospec_hash',
            field=models.CharField(blank=True, help_text='Hash computed from reference source and iospec_size.', max_length=32),
        ),
        migrations.AlterField(
            model_name='answerkeyitem',
            name='source_hash',
            field=models.CharField(blank=True, help_text='Hash computed from the reference source', max_length=32),
        ),
    ]