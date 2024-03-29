# Generated by Django 4.2.7 on 2024-02-03 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0003_offer_delete_job'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='level',
            field=models.CharField(choices=[('Bac', 'Bac'), ('Bac+3', 'Bac+3'), ('Bac+5', 'Bac+5')], max_length=10),
        ),
        migrations.AlterField(
            model_name='offer',
            name='offer_type',
            field=models.CharField(choices=[('Internship', 'intership'), ('Part-time Job', 'part_time_job'), ('Full-time Job', 'full_time_job')], max_length=13),
        ),
        migrations.AlterField(
            model_name='offer',
            name='period',
            field=models.CharField(choices=[('CDD', 'CDD'), ('CDI', 'CDI'), ('Internship_period', 'internship_period')], max_length=17),
        ),
    ]
