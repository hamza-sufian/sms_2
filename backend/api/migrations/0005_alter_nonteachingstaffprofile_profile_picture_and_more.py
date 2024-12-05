# Generated by Django 5.1.1 on 2024-12-05 18:43

import api.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_nonteachingstaffprofile_date_of_employment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nonteachingstaffprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/profile_pictures/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']), api.models.validate_file_size]),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='admission_letter',
            field=models.FileField(blank=True, null=True, upload_to='uploads/admission_letters/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx']), api.models.validate_file_extension, api.models.validate_file_size]),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='medical_forms',
            field=models.FileField(blank=True, null=True, upload_to='uploads/medical_forms/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx']), api.models.validate_file_extension, api.models.validate_file_size]),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='payment_status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('PARTIAL', 'Partial'), ('PAID', 'Paid'), ('OVERDUE', 'Overdue')], default='PENDING', max_length=20),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/profile_pictures/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']), api.models.validate_file_size]),
        ),
        migrations.AlterField(
            model_name='teacherprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/profile_pictures/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']), api.models.validate_file_size]),
        ),
    ]