# Generated by Django 4.2.2 on 2023-06-12 11:35

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Camera',
            fields=[
                ('uid', models.UUIDField(primary_key=True, serialize=False, unique=True)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9, verbose_name='ширина')),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9, verbose_name='дължина')),
                ('rotation', models.DecimalField(decimal_places=6, max_digits=9, verbose_name='ротация спрямо север')),
                ('url', models.URLField(verbose_name='линк')),
                ('parking_mask', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('violator_mask', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('max_cap', models.PositiveIntegerField(default=0)),
                ('current_cap', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Камера',
                'verbose_name_plural': 'Камери',
            },
        ),
    ]
