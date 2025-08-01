# Generated by Django 5.2.3 on 2025-07-08 05:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('master', '0004_leavepolicy'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=False)),
                ('joining_date', models.DateField()),
                ('name', models.CharField(max_length=25)),
                ('email', models.EmailField(max_length=50)),
                ('contact', models.CharField(max_length=10)),
                ('password', models.CharField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='media/')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='department', to='master.department')),
                ('role', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='role', to='master.role')),
                ('team_leader', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='employee.employee')),
            ],
            options={
                'verbose_name_plural': 'Employee',
            },
        ),
    ]
