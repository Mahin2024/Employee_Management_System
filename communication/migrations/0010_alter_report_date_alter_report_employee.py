# Generated by Django 5.2.4 on 2025-07-25 10:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communication', '0009_alter_conversation_room_alter_conversation_sender'),
        ('employee', '0010_alter_leave_options_alter_leave_reason_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employee_report', to='employee.employee'),
        ),
    ]
