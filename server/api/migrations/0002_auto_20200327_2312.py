# Generated by Django 3.0.2 on 2020-03-27 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='designpatentinfo',
            name='category',
            field=models.CharField(default='기타', max_length=64),
        ),
        migrations.AddField(
            model_name='markpatentinfo',
            name='category',
            field=models.CharField(default='기타', max_length=64),
        ),
    ]
