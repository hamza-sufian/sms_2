# Generated by Django 5.1.1 on 2024-12-02 19:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_nonteachingstaffprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacherprofile',
            name='department',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='teacherprofile',
            name='date_of_employment',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
