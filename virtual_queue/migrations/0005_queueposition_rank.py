# Generated by Django 3.1.1 on 2020-11-16 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('virtual_queue', '0004_patient'),
    ]

    operations = [
        migrations.AddField(
            model_name='queueposition',
            name='rank',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]