# Generated by Django 3.0.6 on 2020-05-14 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0002_introduce_collections'),
    ]

    operations = [
        migrations.AddField(
            model_name='pollcollection',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
    ]
