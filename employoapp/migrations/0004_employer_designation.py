# Generated by Django 2.1.7 on 2019-05-17 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employoapp', '0003_auto_20190517_1711'),
    ]

    operations = [
        migrations.AddField(
            model_name='employer',
            name='designation',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]