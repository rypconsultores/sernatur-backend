# Generated by Django 3.1.3 on 2020-12-19 05:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('c19trace', '0009_place_person_check'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserExtraConf',
            fields=[
                ('traceability', models.BooleanField(default=False, verbose_name='Tracabilidad')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='user_extra_conf', serialize=False, to='auth.user', verbose_name='user')),
            ],
            options={
                'verbose_name': 'User extra config',
                'verbose_name_plural': 'User extra config',
                'db_table': 'c19t_user_extra_conf',
            },
        ),
    ]
