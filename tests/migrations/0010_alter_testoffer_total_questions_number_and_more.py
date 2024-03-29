# Generated by Django 4.2.7 on 2024-02-20 09:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_delete_administrator'),
        ('tests', '0009_testoffer_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testoffer',
            name='total_questions_number',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_results_student', to='users.studentprofile'),
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(default=False, editable=False)),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_session', to='tests.testoffer')),
            ],
        ),
        migrations.AddField(
            model_name='candidateanswer',
            name='session',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='exam_session', to='tests.session'),
        ),
        migrations.AddField(
            model_name='testresult',
            name='session',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='test_results_session', to='tests.session'),
        ),
    ]
