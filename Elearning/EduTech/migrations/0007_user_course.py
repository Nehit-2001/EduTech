# Generated by Django 4.2.3 on 2023-09-04 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EduTech', '0006_tag_prereq_learning'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EduTech.course_details')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EduTech.signup')),
            ],
        ),
    ]
