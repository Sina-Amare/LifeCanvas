# Generated by Django 5.1.6 on 2025-04-29 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0002_alter_journal_mood'),
    ]

    operations = [
        migrations.AddField(
            model_name='journal',
            name='labels',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name='journal',
            name='location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
