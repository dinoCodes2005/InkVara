# Generated by Django 5.1.3 on 2025-02-23 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogarea', '0045_alter_post_articlesnippet'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(blank=True, max_length=20, null=True)),
                ('post', models.ManyToManyField(null=True, related_name='tagged_post', to='blogarea.post')),
            ],
        ),
    ]
