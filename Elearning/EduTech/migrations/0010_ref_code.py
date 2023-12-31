# Generated by Django 4.2.3 on 2023-09-14 13:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EduTech', '0009_alter_payment_course_info'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ref_code',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('discount', models.IntegerField(default=0)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EduTech.course_details')),
            ],
        ),
    ]
