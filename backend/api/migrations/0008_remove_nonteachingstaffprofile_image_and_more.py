# Generated by Django 5.1.1 on 2024-12-03 18:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_user_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nonteachingstaffprofile',
            name='image',
        ),
        migrations.RemoveField(
            model_name='studentprofile',
            name='profile_image',
        ),
        migrations.RemoveField(
            model_name='teacherprofile',
            name='image',
        ),
    ]
