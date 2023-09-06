# Generated by Django 4.2.3 on 2023-08-29 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Signup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='', max_length=100, null=True)),
                ('last_name', models.CharField(default='', max_length=100, null=True)),
                ('email', models.CharField(default='', max_length=100, null=True)),
                ('password', models.CharField(default='', max_length=255, null=True)),
                ('mobile', models.BigIntegerField(null=True)),
                ('gender', models.CharField(default='', max_length=100, null=True)),
            ],
        ),
    ]
