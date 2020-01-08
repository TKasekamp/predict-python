# Generated by Django 2.2.7 on 2019-12-25 20:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clustering',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_path', models.FilePathField(path='cache/model_cache/')),
                ('clustering_method', models.CharField(choices=[('kmeans', 'kmeans'), ('noCluster', 'noCluster')], max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='KMeans',
            fields=[
                ('clustering_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='clustering.Clustering')),
                ('n_clusters', models.PositiveIntegerField()),
                ('init', models.CharField(choices=[('k-means++', 'k-means++'), ('random', 'random')], default='k-means++', max_length=10)),
                ('n_init', models.PositiveIntegerField(blank=True, null=True)),
                ('max_iter', models.PositiveIntegerField(blank=True, null=True)),
                ('tol', models.FloatField(blank=True, null=True)),
                ('precompute_distances', models.CharField(choices=[(True, 'True'), (False, 'False'), ('auto', 'auto')], default='auto', max_length=6)),
                ('random_state', models.PositiveIntegerField(blank=True, null=True)),
                ('copy_x', models.BooleanField(blank=True, null=True)),
                ('algorithm', models.CharField(choices=[('auto', 'auto'), ('full', 'full'), ('elkan', 'elkan')], default='auto', max_length=6)),
            ],
            options={
                'abstract': False,
            },
            bases=('clustering.clustering',),
        ),
        migrations.CreateModel(
            name='NoCluster',
            fields=[
                ('clustering_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='clustering.Clustering')),
            ],
            options={
                'abstract': False,
            },
            bases=('clustering.clustering',),
        ),
    ]