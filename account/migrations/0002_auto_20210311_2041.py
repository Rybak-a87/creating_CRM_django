# Generated by Django 3.1.7 on 2021-03-11 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='manager_status',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Вы менеджер?'),
        ),
    ]
