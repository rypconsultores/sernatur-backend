# Generated by Django 3.1.3 on 2021-01-03 07:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('c19trace', '0012_revision_02'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='placepersonchecksymptom',
            name='temperature',
        ),
        migrations.AddField(
            model_name='placepersoncheck',
            name='is_customer',
            field=models.BooleanField(default=False, verbose_name='Es cliente'),
        ),
        migrations.AddField(
            model_name='placepersoncheck',
            name='is_employee',
            field=models.BooleanField(default=False, verbose_name='Es trabajador'),
        ),
        migrations.AddField(
            model_name='placepersoncheck',
            name='is_provider',
            field=models.BooleanField(default=False, verbose_name='Es proovedor'),
        ),
        migrations.AlterField(
            model_name='person',
            name='contact_name',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Contact Name'),
        ),
        migrations.AlterField(
            model_name='person',
            name='contact_phone_or_email',
            field=models.CharField(blank=True, max_length=24, null=True, verbose_name='Contact phone or email'),
        ),
        migrations.AlterField(
            model_name='person',
            name='contact_relationship',
            field=models.CharField(blank=True, choices=[('familiar/amigo', 'Family/Friend'), ('travel agency', 'Travel Agency'), ('tour operator', 'Tour Operator'), ('empresa (negocios o trabajo)', 'Company (Business or Work)'), ('ninguno', 'None')], help_text='Opciones:\n- familiar/amigo: Family/Friend\n- travel agency: Agencia de viajes\n- tour operator: Operador de tour\n- empresa (negocios o trabajo): Empresa (Negocios or trabajo)\n- ninguno: Ninguno\n* Tambien puede ser llenado con una entrada personalizada', max_length=48, null=True, verbose_name='Contact replationship'),
        ),
        migrations.AlterField(
            model_name='person',
            name='destination',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Destination'),
        ),
        migrations.AlterField(
            model_name='person',
            name='entry_point',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='c19trace.entrypoint', verbose_name='Entry point'),
        ),
        migrations.AlterField(
            model_name='person',
            name='main_transportation_mean',
            field=models.CharField(blank=True, choices=[('Motocicleta', 'Motorcycle'), ('Bicicleta', 'Bycicle'), ('Auto/Jeep/Camioneta', 'Car/Jeep/Pickup truck'), ('Motorhome/Casa Rodante', 'Motorhome'), ('Bus', 'Bus'), ('Camión', 'Truck')], help_text='Opciones:\n- Motocicleta: Moto\n- Bicicleta: Bicicleta\n- Auto/Jeep/Camioneta: Automóvil/Jeep/Camioneta\n- Motorhome/Casa Rodante: Casa rodante/Motorhome\n- Bus: Bus\n- Camión: Camion\n* Tambien puede ser llenado con una entrada personalizada', max_length=64, null=True, verbose_name='Main transportation mean'),
        ),
        migrations.AlterField(
            model_name='person',
            name='previous_lodging_place',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Previous lodging place'),
        ),
        migrations.AlterField(
            model_name='person',
            name='transportation_mode',
            field=models.CharField(blank=True, choices=[('agua', 'Water'), ('aire', 'Air'), ('tierra', 'Land')], help_text='Opciones:\n- agua: Agua\n- aire: Aire\n- tierra: tierra', max_length=8, null=True, verbose_name='Transportation mode'),
        ),
        migrations.AlterField(
            model_name='person',
            name='visit_no',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name='Visit number'),
        ),
        migrations.AlterField(
            model_name='person',
            name='visit_subject',
            field=models.CharField(blank=True, choices=[('turismo', 'Turism'), ('vacaciones', 'Vacations'), ('visita familiares/amigos', 'Visit to family or friend'), ('trabajo', 'Work'), ('negocios', 'Business'), ('other', 'Other')], max_length=128, null=True, verbose_name='Visit subject'),
        ),
        migrations.AlterField(
            model_name='underageperson',
            name='relationship',
            field=models.CharField(choices=[('amigo/a', 'Friend'), ('cuñado/a', 'Sibling in law'), ('hermano/a', 'sibling'), ('hijo/a', 'Child'), ('nieto/a', 'Grandchild'), ('primo/a', 'Cousin'), ('sobrino/a', 'Nephew'), ('tio/a', 'Uncle/aunt')], help_text='Opciones:\n- amigo/a: Amiga/o\n- cuñado/a: Cuñada/o\n- hermano/a: hermanoa/o\n- hijo/a: Hija/o\n- nieto/a: Nieta/o\n- primo/a: Prima/o\n- sobrino/a: Sobrina/o\n- tio/a: Tía/Tío\n* Tambien puede ser llenado con una entrada personalizada', max_length=24, verbose_name='Contact replationship'),
        ),
    ]