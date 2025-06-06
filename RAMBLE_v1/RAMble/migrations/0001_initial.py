# Generated by Django 4.2 on 2025-06-02 03:53

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
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('rating', models.FloatField(default=0.0)),
                ('rate_per_hour', models.DecimalField(decimal_places=2, max_digits=6)),
                ('about', models.TextField(blank=True, default='This tutor has not added a description yet.')),
                ('subjects', models.ManyToManyField(related_name='tutors', to='RAMble.subject')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TutorAvailability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time_slot', models.TimeField(blank=True, null=True)),
                ('is_available', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('tutor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='availabilities', to='RAMble.tutor')),
            ],
            options={
                'unique_together': {('tutor', 'date', 'time_slot')},
            },
        ),
    ]
