# Generated by Django 3.1.3 on 2021-01-07 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_profile_spec'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='json_spec',
            field=models.TextField(default=dict),
        ),
    ]
