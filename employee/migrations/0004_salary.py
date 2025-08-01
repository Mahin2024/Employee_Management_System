# Generated by Django 5.2.3 on 2025-07-08 07:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0003_alter_attendance_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=False)),
                ('amount', models.IntegerField()),
                ('bonus', models.IntegerField(blank=True, null=True)),
                ('deductions', models.IntegerField(blank=True, null=True)),
                ('net_salary', models.IntegerField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_salary', to='employee.employee')),
            ],
            options={
                'verbose_name_plural': 'Salary',
            },
        ),
    ]
