# Generated by Django 3.1.3 on 2021-01-07 13:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20210107_1239'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='spec',
        ),
    ]
