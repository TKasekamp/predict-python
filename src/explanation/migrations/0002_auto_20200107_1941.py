# Generated by Django 2.2.7 on 2020-01-07 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('explanation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='explanation',
            name='type',
            field=models.CharField(blank=True, choices=[('shap', 'shap'), ('lime', 'lime'), ('anchor', 'anchor'), ('pred', 'pred')], default='shap', max_length=7, null=True),
        ),
    ]