# Generated by Django 4.2.7 on 2024-02-20 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0015_alter_session_period'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='key',
            field=models.CharField(editable=False, max_length=64),
        ),
    ]
