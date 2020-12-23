# Generated by Django 3.1.3 on 2020-12-23 08:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('c19trace', '0011_revision_01'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='document_no',
            field=models.CharField(max_length=128, unique=True, verbose_name='Document Number'),
        ),
        migrations.AlterField(
            model_name='person',
            name='id',
            field=models.CharField(default='__auto__', max_length=64, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='person',
            name='visit_no',
            field=models.IntegerField(blank=True, null=True, verbose_name='Visit number'),
        ),
        migrations.AlterField(
            model_name='place',
            name='service_class',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='c19trace.turisticserviceclass', verbose_name='Service class'),
        ),
        migrations.AlterField(
            model_name='place',
            name='service_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='c19trace.turisticservicetype', verbose_name='Service type'),
        ),
    ]