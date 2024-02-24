# Generated by Django 4.2.7 on 2024-02-02 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('company', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('level', models.CharField(choices=[('bac', 'Bac'), ('bac+3', 'Bac+3'), ('bac+5', 'Bac+5'), ('more', 'More')], max_length=10)),
                ('salary', models.PositiveIntegerField()),
                ('job_type', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('posted_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]