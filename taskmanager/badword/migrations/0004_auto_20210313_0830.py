# Generated by Django 3.1.7 on 2021-03-13 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('badword', '0003_auto_20210313_0827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='textmodel',
            name='title',
            field=models.TextField(unique=True, verbose_name='Название'),
        ),
    ]