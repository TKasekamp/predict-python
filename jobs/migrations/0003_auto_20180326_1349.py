# Generated by Django 2.0.3 on 2018-03-26 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_jobrun'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobrun',
            name='log',
        ),
        migrations.AddField(
            model_name='job',
            name='run',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='JobRun',
        ),
    ]
