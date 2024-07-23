# Generated by Django 5.0.6 on 2024-07-23 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_vente_montant_alter_vente_vendeur'),
    ]

    operations = [
        migrations.AddField(
            model_name='brouillardcaisse',
            name='solde_initial',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='brouillardcaisse',
            name='solde',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
