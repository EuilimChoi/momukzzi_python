# Generated by Django 4.0.6 on 2022-07-25 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawling', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoppic',
            name='URL',
            field=models.TextField(),
        ),
    ]