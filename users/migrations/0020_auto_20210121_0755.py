# Generated by Django 3.1.3 on 2021-01-21 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_auto_20210121_0747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='json_spec',
            field=models.TextField(default=dict),
        ),
    ]
