# Generated by Django 4.0.4 on 2023-03-07 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managers', '0005_alter_document_client_alter_document_request_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='document',
            field=models.FileField(upload_to='./managers/files'),
        ),
    ]
