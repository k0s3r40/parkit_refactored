# Generated by Django 4.2.2 on 2023-06-26 18:28

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cameras', '0005_remove_camera_rotation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='camera',
            name='parking_mask',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, null=True, srid=4326),
        ),
        migrations.AlterField(
            model_name='camera',
            name='violator_mask',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, null=True, srid=4326),
        ),
    ]
