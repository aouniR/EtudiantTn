# Generated by Django 4.2.7 on 2024-02-06 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rent', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rentoffer',
            name='phone',
            field=models.CharField(blank=True, max_length=8),
        ),
        migrations.AlterField(
            model_name='rentoffer',
            name='rooms',
            field=models.CharField(choices=[('S+0', 'S+0'), ('S+1', 'S+1'), ('S+2', 'S+2'), ('S+3', 'S+3'), ('Extra', 'Extra')], max_length=10),
        ),
    ]
