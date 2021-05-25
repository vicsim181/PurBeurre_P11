# Generated by Django 2.2.12 on 2021-04-29 09:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('page_number', models.IntegerField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('nutriscore', models.CharField(max_length=1)),
                ('description', models.TextField()),
                ('url', models.CharField(max_length=200)),
                ('popularity', models.IntegerField()),
                ('salt', models.CharField(max_length=10)),
                ('sugars', models.CharField(max_length=10)),
                ('saturated', models.CharField(max_length=10)),
                ('fat', models.CharField(max_length=10)),
                ('image_url', models.CharField(max_length=100)),
                ('small_image_url', models.CharField(max_length=100)),
                ('category', models.ManyToManyField(to='main.Category')),
                ('store', models.ManyToManyField(to='main.Store')),
            ],
        ),
    ]
