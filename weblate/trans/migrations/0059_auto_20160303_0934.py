# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-03 09:34
from __future__ import unicode_literals

from django.db import migrations


def fill_in_subscriptions(apps, schema_editor):
    """Adds subscriptions to owners or ACL enabled users"""
    Project = apps.get_model('trans', 'Project')
    Group = apps.get_model('auth', 'Group')
    Profile = apps.get_model('accounts', 'Profile')

    for project in Project.objects.all():
        for owner in project.owners.all():
            try:
                owner.profile.subscriptions.add(project)
            except Profile.DoesNotExist:
                pass

        if project.enable_acl:
            group = Group.objects.get(name=project.name)
            for user in group.user_set.all():
                try:
                    user.profile.subscriptions.add(project)
                except Profile.DoesNotExist:
                    pass


class Migration(migrations.Migration):

    dependencies = [
        ('trans', '0058_componentlist'),
    ]

    operations = [
        migrations.RunPython(
            fill_in_subscriptions,
        ),
    ]
