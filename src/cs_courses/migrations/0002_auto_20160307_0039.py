# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-07 00:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cs_courses', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='timeslot',
            old_name='end_time',
            new_name='end',
        ),
        migrations.RenameField(
            model_name='timeslot',
            old_name='start_time',
            new_name='start',
        ),
        migrations.RemoveField(
            model_name='course',
            name='course_end',
        ),
        migrations.RemoveField(
            model_name='course',
            name='course_start',
        ),
        migrations.RemoveField(
            model_name='course',
            name='timestamp',
        ),
        migrations.AddField(
            model_name='course',
            name='created',
            field=model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created'),
        ),
        migrations.AddField(
            model_name='course',
            name='end',
            field=models.DateTimeField(blank=True, null=True, verbose_name='end'),
        ),
        migrations.AddField(
            model_name='course',
            name='modified',
            field=model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified'),
        ),
        migrations.AddField(
            model_name='course',
            name='start',
            field=models.DateTimeField(blank=True, null=True, verbose_name='start'),
        ),
    ]