# Generated by Django 3.2 on 2021-05-01 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JobTrackingApp', '0009_alter_scheduleevent_duration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scheduleevent',
            name='user',
        ),
        migrations.AlterField(
            model_name='scheduleevent',
            name='description',
            field=models.TextField(blank=True, max_length=2000),
        ),
    ]
