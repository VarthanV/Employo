# Generated by Django 2.1.7 on 2019-05-17 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employoapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skill',
            name='skill',
            field=models.TextField(),
        ),
    ]