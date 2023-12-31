# Generated by Django 4.2.2 on 2023-07-01 12:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
                ('question', models.TextField()),
                ('questionHTML', models.TextField()),
                ('solution', models.TextField()),
                ('test_case', models.TextField()),
                ('start_snippet', models.TextField()),
                ('question_verified', models.BooleanField(default=False)),
                ('upload_time', models.DateTimeField(auto_now_add=True)),
                ('difficulty', models.CharField(choices=[('HARD', 'HARD'), ('MEDIUM', 'MEDIUM'), ('EASY', 'EASY')], default='EASY', max_length=20)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('users_attempted', models.ManyToManyField(blank=True, related_name='users_attempted', to=settings.AUTH_USER_MODEL)),
                ('users_completed', models.ManyToManyField(blank=True, related_name='users_completed', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField()),
                ('answer_time', models.DateTimeField(auto_now_add=True)),
                ('upload_time', models.DateTimeField(auto_now_add=True)),
                ('tests_pass', models.BooleanField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='challenges.question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
