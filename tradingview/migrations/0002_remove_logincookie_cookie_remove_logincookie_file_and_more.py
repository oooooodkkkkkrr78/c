# Generated by Django 4.1.2 on 2022-10-23 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tradingview', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logincookie',
            name='cookie',
        ),
        migrations.RemoveField(
            model_name='logincookie',
            name='file',
        ),
        migrations.AddField(
            model_name='logincookie',
            name='cookies',
            field=models.TextField(blank=True, editable=False, null=True, verbose_name='اطلاعات کوکی'),
        ),
    ]
