# Generated by Django 3.1.3 on 2020-12-17 07:16

import apps.c19trace.models.util
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('c19trace', '0008_initial_rev_07'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlacePersonCheckSymptom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cough', models.BooleanField(default=False, verbose_name='Cough')),
                ('dispnea', models.BooleanField(default=False, verbose_name='Dispnea or breathing difficulty')),
                ('thoracic_pain', models.BooleanField(default=False, verbose_name='Throracic pain')),
                ('throat_pain', models.BooleanField(default=False, verbose_name='Throat pain or odynophagia')),
                ('muscular_articular_pain', models.BooleanField(default=False, verbose_name='Myalgia, muscular or articular pain')),
                ('chills', models.BooleanField(default=False, verbose_name='Chills')),
                ('headache', models.BooleanField(default=False, verbose_name='Headache')),
                ('diarrhea', models.BooleanField(default=False, verbose_name='Diarrhea')),
                ('lost_smell', models.BooleanField(default=False, verbose_name='Abrupt lost of smell')),
                ('lost_taste', models.BooleanField(default=False, verbose_name='Abrupt lost of taste')),
                ('fever', models.BooleanField(default=False, verbose_name='fever')),
            ],
        ),
        migrations.CreateModel(
            name='PlacePersonCheck',
            fields=[
                ('id', models.CharField(max_length=64, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(default=apps.c19trace.models.util.thenow, verbose_name='Creation date')),
                ('modification_date', models.DateTimeField(default=apps.c19trace.models.util.thenow, verbose_name='Modification date')),
                ('observations', models.TextField(blank=True, null=True, verbose_name='Observations')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='c19trace.person', verbose_name='Person')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='c19trace.place', verbose_name='Place')),
                ('place_check_point', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='c19trace.placecheckpoint', verbose_name='Place')),
                ('symptoms', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, to='c19trace.placepersonchecksymptom', verbose_name='Symptoms')),
            ],
            options={
                'verbose_name': 'Place person check',
                'verbose_name_plural': 'Place persons checks',
                'db_table': 'c19t_place_persons_checks',
                'ordering': ('creation_date',),
            },
        ),
    ]