# Generated by Django 4.0.6 on 2022-07-27 08:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crawling', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopmenu',
            name='shopId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crawling.shopinfo'),
        ),
        migrations.AlterField(
            model_name='shoppic',
            name='shopId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crawling.shopinfo'),
        ),
    ]
