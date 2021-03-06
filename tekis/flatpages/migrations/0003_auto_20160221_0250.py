# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-21 00:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flatpages', '0002_auto_20160221_0006'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('url', models.URLField()),
                ('logo', models.ImageField(upload_to='sponsors/')),
                ('titletext', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.AlterField(
            model_name='flatpage',
            name='menu_index',
            field=models.IntegerField(default=0, help_text='Menus are sorted ascending by this value. The first menu item in a category is the category link itself. <strong>Note:</strong> The first menu item in the top level category should be the front page.'),
        ),
        migrations.AlterField(
            model_name='flatpage',
            name='published',
            field=models.BooleanField(default=False, help_text='Published pages show up on the menu. Unpublished pages can be reached over direct link.'),
        ),
    ]
