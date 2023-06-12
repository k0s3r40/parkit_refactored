# Generated by Django 4.2.2 on 2023-06-12 16:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_managers'),
        ('cameras', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='camera',
            name='organization',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='users.organization'),
            preserve_default=False,
        ),
    ]
