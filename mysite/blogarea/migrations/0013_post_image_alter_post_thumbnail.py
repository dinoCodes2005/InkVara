# Generated by Django 5.1.3 on 2025-01-17 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogarea', '0012_alter_post_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='blogPostImages/'),
        ),
        migrations.AlterField(
            model_name='post',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='thumbnail/'),
        ),
    ]
