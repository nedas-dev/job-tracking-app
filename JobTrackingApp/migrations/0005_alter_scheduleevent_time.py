# Generated by Django 3.2 on 2021-05-01 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JobTrackingApp', '0004_scheduleevent_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduleevent',
            name='time',
            field=models.DurationField(null=True),
        ),
    ]
