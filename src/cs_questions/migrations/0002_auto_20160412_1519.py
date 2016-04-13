# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-12 18:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cs_questions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='owner',
            field=models.ForeignKey(blank=True, help_text='User who created or uploaded this question.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='codingioquestion',
            name='status',
            field=model_utils.fields.StatusField(choices=[(0, 'dummy')], default='incomplete', max_length=100, no_check_for_status=True, verbose_name='status'),
        ),
    ]