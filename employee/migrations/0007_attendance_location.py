# Generated by Django 5.2.3 on 2025-07-11 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0006_alter_attendance_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='location',
            field=models.CharField(blank=True, choices=[('WFH', 'WFH'), ('WFO', 'WFO')], null=True),
        ),
    ]
