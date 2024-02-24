# Generated by Django 4.2.7 on 2024-02-20 09:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0010_alter_testoffer_total_questions_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidateanswer',
            name='session',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='exam_session', to='tests.session'),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='session',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='test_results_session', to='tests.session'),
        ),
    ]