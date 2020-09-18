# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('course_name', models.CharField(max_length=200)),
                ('duration', models.CharField(max_length=50)),
                ('course_fee', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('firstname', models.CharField(max_length=100, null=True, blank=True)),
                ('lastname', models.CharField(max_length=100, null=True, blank=True)),
                ('mobile', models.CharField(max_length=10, null=True, blank=True)),
                ('gender', models.CharField(max_length=20, choices=[(b'Male', b'Male'), (b'Female', b'Female')])),
                ('email', models.CharField(max_length=40, null=True, blank=True)),
                ('age', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='StudentCourse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(max_length=20, choices=[(b'accepted', b'accepted'), (b'rejected', b'rejected'), (b'under progressive', b'under progressive')])),
                ('enroll_date', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(to='student.Course')),
                ('student', models.ForeignKey(to='student.Student')),
            ],
        ),
    ]
