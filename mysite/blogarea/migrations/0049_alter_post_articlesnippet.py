# Generated by Django 5.1.3 on 2025-02-23 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogarea', '0048_alter_post_hashtags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='articleSnippet',
            field=models.CharField(max_length=50),
        ),
    ]
