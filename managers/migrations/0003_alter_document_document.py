# Generated by Django 4.0.4 on 2023-03-06 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managers', '0002_document_request'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='document',
            field=models.FileField(upload_to='./files'),
        ),
    ]
