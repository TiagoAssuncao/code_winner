# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-01 02:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cs_questions', '0016_auto_20160531_1924'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quizactivity',
            old_name='grading_method',
            new_name='quiz_grading_method',
        ),
    ]