# Generated by Django 4.2.7 on 2024-02-20 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0014_remove_session_end_time_session_period'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='period',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
    ]
