# Generated by Django 5.2 on 2025-04-27 04:01

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_homework_topshiriq'),
    ]

    operations = [
        migrations.CreateModel(
            name='Month',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_ed', models.DateField(auto_now_add=True)),
                ('updated_ed', models.DateField(auto_now=True)),
                ('month_number', models.PositiveSmallIntegerField(choices=[(1, 'Yanvar'), (2, 'Fevral'), (3, 'Mart'), (4, 'Aprel'), (5, 'May'), (6, 'Iyun'), (7, 'Iyul'), (8, 'Avgust'), (9, 'Sentabr'), (10, 'Oktabr'), (11, 'Noyabr'), (12, 'Dekabr')], validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)], verbose_name='oy raqami')),
                ('year', models.PositiveIntegerField(verbose_name='yil')),
                ('name', models.CharField(editable=False, max_length=25, verbose_name='oy nomi')),
                ('start_date', models.DateField(verbose_name='boshlanish sanasi')),
                ('end_date', models.DateField(verbose_name='tugash vaqti')),
                ('description', models.TextField(blank=True, null=True, verbose_name='qoshimcha malumot')),
            ],
            options={
                'verbose_name': 'oy',
                'verbose_name_plural': 'oylar',
                'ordering': ['year', 'month_number'],
                'unique_together': {('month_number', 'year')},
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_ed', models.DateField(auto_now_add=True)),
                ('updated_ed', models.DateField(auto_now=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12, verbose_name="To'lov miqdori")),
                ('status', models.CharField(choices=[('paid', "To'langan"), ('unpaid', "To'lanmagan"), ('partial', "Qisman to'langan"), ('cancelled', 'Bekor qilingan')], default='unpaid', max_length=20)),
                ('payment_method', models.CharField(blank=True, choices=[('cash', 'Naqd pul'), ('card', 'Bank kartasi'), ('transfer', "Bank o'tkazmasi"), ('click', 'Click'), ('payme', 'Payme')], max_length=20, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('payment_date', models.DateField(blank=True, null=True, verbose_name="To'lov sanasi")),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='app.groupstudent')),
                ('month', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='app.month')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='app.student')),
            ],
            options={
                'verbose_name': "To'lov",
                'verbose_name_plural': "To'lovlar",
                'ordering': ['-payment_date'],
            },
        ),
    ]
