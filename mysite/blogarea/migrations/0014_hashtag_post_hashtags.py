# Generated by Django 5.1.3 on 2025-01-17 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogarea', '0013_post_image_alter_post_thumbnail'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='hashtags',
            field=models.ManyToManyField(blank=True, related_name='post', to='blogarea.hashtag'),
        ),
    ]
