# Generated by Django 5.1.3 on 2025-02-23 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogarea', '0049_alter_post_articlesnippet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hashtag',
            name='post',
            field=models.ManyToManyField(null=True, related_name='hashtag_posts', to='blogarea.post'),
        ),
    ]
