# Generated by Django 2.1.7 on 2019-05-19 05:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employoapp', '0009_auto_20190518_1319'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_file', models.FileField(upload_to='')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employoapp.Jobs')),
            ],
        ),
    ]
