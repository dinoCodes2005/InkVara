# Generated by Django 5.1.3 on 2025-01-17 07:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogarea', '0008_category_post_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
    ]
