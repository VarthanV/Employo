# Generated by Django 2.1.7 on 2019-05-27 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employoapp', '0018_auto_20190521_1154'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobfiles',
            name='job',
        ),
        migrations.AddField(
            model_name='jobfiles',
            name='job',
            field=models.ManyToManyField(related_name='jobs_set', to='employoapp.Jobs'),
        ),
    ]
