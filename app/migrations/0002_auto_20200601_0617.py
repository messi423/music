# Generated by Django 3.0.6 on 2020-05-31 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='logo',
            field=models.FileField(upload_to='app'),
        ),
        migrations.AlterField(
            model_name='song',
            name='audio',
            field=models.FileField(upload_to='app'),
        ),
    ]
