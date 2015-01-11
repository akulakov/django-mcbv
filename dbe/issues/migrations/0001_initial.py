# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('body', models.TextField(default=b'', max_length=3000, blank=True)),
                ('body_html', models.TextField(null=True, blank=True)),
                ('priority', models.IntegerField(default=0, null=True, blank=True)),
                ('difficulty', models.IntegerField(default=0, null=True, blank=True)),
                ('progress', models.IntegerField(default=0)),
                ('closed', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(related_name='created_issues', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('owner', models.ForeignKey(related_name='issues', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IssueComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('body', models.TextField(max_length=3000)),
                ('body_html', models.TextField()),
                ('creator', models.ForeignKey(related_name='comments', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('issue', models.ForeignKey(related_name='comments', blank=True, to='issues.Issue', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IssueTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag', models.CharField(max_length=30)),
                ('creator', models.ForeignKey(related_name='tags', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project', models.CharField(max_length=60)),
                ('creator', models.ForeignKey(related_name='projects', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='issue',
            name='project',
            field=models.ForeignKey(related_name='issues', blank=True, to='issues.Project', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='issue',
            name='tags',
            field=models.ManyToManyField(related_name='issues', null=True, to='issues.IssueTag', blank=True),
            preserve_default=True,
        ),
    ]
