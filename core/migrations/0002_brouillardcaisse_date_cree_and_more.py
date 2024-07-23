# Generated by Django 5.0.6 on 2024-07-22 16:10

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='brouillardcaisse',
            name='date_cree',
            field=models.DateTimeField(auto_created=True, auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='brouillardcaisse',
            name='date_modifie',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='sortie',
            name='date_cree',
            field=models.DateTimeField(auto_created=True, auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sortie',
            name='date_modifie',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='vente',
            name='date_cree',
            field=models.DateTimeField(auto_created=True, auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vente',
            name='date_modifie',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
