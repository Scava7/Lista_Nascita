# Generated by Django 5.2.1 on 2025-05-08 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lista', '0002_regalo_immagine'),
    ]

    operations = [
        migrations.AddField(
            model_name='regalo',
            name='link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
