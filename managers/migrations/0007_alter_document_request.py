# Generated by Django 4.0.4 on 2023-03-07 15:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('managers', '0006_alter_document_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='request',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='managers.request'),
        ),
    ]
