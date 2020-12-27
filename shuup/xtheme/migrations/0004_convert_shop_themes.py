# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2016-12-07 23:22
from __future__ import unicode_literals

from django.db.transaction import atomic
from django.db import migrations

from shuup.core.models import Shop
from shuup.xtheme.models import SavedViewConfig, ThemeSettings


@atomic
def convert_shop_themes(*args):
    for theme_setting in ThemeSettings.objects.filter(shop__isnull=True):

        for (index, shop) in enumerate(Shop.objects.all()):
            # already exists.. ignore
            if ThemeSettings.objects.filter(shop=shop, theme_identifier=theme_setting.theme_identifier).exists():
                continue

            # the first shop received the original object, the other, are just copies
            if index > 0:
                theme_setting.pk = None

            theme_setting.shop = shop
            theme_setting.save()


    for saved_config in SavedViewConfig.objects.filter(shop__isnull=True):
        for (index, shop) in enumerate(Shop.objects.all()):
            # already exists.. ignore
            if SavedViewConfig.objects.filter(shop=shop, theme_identifier=saved_config.theme_identifier).exists():
                continue

            # the first shop received the original object, the other, are just copies
            if index > 0:
                saved_config.pk = None

            saved_config.shop = shop
            saved_config.save()


class Migration(migrations.Migration):

    dependencies = [
        ('shuup_xtheme', '0003_shop_theme'),
    ]

    operations = [
        migrations.RunPython(convert_shop_themes, migrations.RunPython.noop)
    ]
