# Generated by Django 2.1.2 on 2018-11-25 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curry_order', '0004_curry_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.CharField(max_length=20, unique=True)),
                ('url_uuid', models.TextField(unique=True)),
            ],
        ),
    ]
