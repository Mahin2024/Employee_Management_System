# Generated by Django 5.2.3 on 2025-07-16 09:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0008_alter_attendance_checkin_alter_attendance_status'),
        ('master', '0004_leavepolicy'),
    ]

    operations = [
        migrations.CreateModel(
            name='Leave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('rejected', 'rejected'), ('approved', 'approved'), ('pending', 'pending')], default='pending')),
                ('type', models.CharField(blank=True, choices=[('half_day', 'half_day'), ('full_day', 'full_day')], null=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('is_paid', models.BooleanField(default=False)),
                ('reason', models.CharField(blank=True, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_leave', to='employee.employee')),
                ('policies', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='policy', to='master.leavepolicy')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
