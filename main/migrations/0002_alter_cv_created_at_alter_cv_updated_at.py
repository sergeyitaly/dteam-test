# Generated by Django 4.2.21 on 2025-06-02 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cv',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='cv',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
