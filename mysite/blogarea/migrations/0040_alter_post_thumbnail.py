# Generated by Django 5.1.3 on 2025-02-14 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogarea', '0039_profile_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='thumbnail',
            field=models.ImageField(blank=True, default='/media/thumbnail/thumbnail.jpg', null=True, upload_to='thumbnail/'),
        ),
    ]
