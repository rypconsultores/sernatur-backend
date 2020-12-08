# Generated by Django 3.1.3 on 2020-12-06 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('c19trace', '0003_initial_rev_02'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrypoint',
            name='type',
            field=models.CharField(choices=[('maritimo', 'Maritime'), ('aereo', 'Aereal'), ('terrestre', 'Ground')], help_text='Opciones:\n- maritimo: Maritimo\n- aereo: Aereo\n- terrestre: Terrestre', max_length=64, verbose_name='Transportation mode'),
        ),
        migrations.AlterField(
            model_name='person',
            name='contact_relationship',
            field=models.CharField(choices=[('abuelo/a', 'Grandparent'), ('amigo/a', 'Friend'), ('colega', 'Colegue'), ('cuñado/a', 'Sibling in law'), ('hermano/a', 'sibling'), ('hijo/a', 'Child'), ('nieto/a', 'Grandchild'), ('padre/madre', 'Parent'), ('primo/a', 'Cousin'), ('sobrino/a', 'Nephew'), ('suegro/a', 'Parent in law'), ('tio/a', 'Uncle/aunt')], help_text='Opciones:\n- abuelo/a: Abuela/o\n- amigo/a: Amiga/o\n- colega: Colega\n- cuñado/a: Cuñada/o\n- hermano/a: hermanoa/o\n- hijo/a: Hija/o\n- nieto/a: Nieta/o\n- padre/madre: Madre/Padre\n- primo/a: Prima/o\n- sobrino/a: Sobrina/o\n- suegro/a: Suegra/o\n- tio/a: Tía/Tío\n* Tambien puede ser llenado con una entrada personalizada', max_length=24, verbose_name='Contact replationship'),
        ),
        migrations.AlterField(
            model_name='person',
            name='destination',
            field=models.CharField(max_length=128, verbose_name='Destination'),
        ),
        migrations.AlterField(
            model_name='person',
            name='gender',
            field=models.CharField(choices=[('Masculino', 'Male'), ('Femenino', 'Female'), ('Otro', 'Other')], help_text='Opciones:\n- Masculino: Masculino\n- Femenino: Femenino\n- Otro: Otro', max_length=24, verbose_name='Gender'),
        ),
        migrations.AlterField(
            model_name='person',
            name='main_transportation_mean',
            field=models.CharField(choices=[('Motocicleta', 'Motorcycle'), ('Bicicleta', 'Bycicle'), ('Auto/Jeep/Camioneta', 'Car/Jeep/Pickup truck'), ('Motorhome/Casa Rodante', 'Motorhome'), ('Bus', 'Bus'), ('Camión', 'Truck')], help_text='Opciones:\n- Motocicleta: Moto\n- Bicicleta: Bicicleta\n- Auto/Jeep/Camioneta: Automóvil/Jeep/Camioneta\n- Motorhome/Casa Rodante: Casa rodante/Motorhome\n- Bus: Bus\n- Camión: Camion\n* Tambien puede ser llenado con una entrada personalizada', max_length=64, verbose_name='Main transportation mean'),
        ),
        migrations.AlterField(
            model_name='person',
            name='residence',
            field=models.CharField(choices=[('Chile', 'Chile'), ('extranjero', 'Not Chile')], help_text='Opciones:\n- Chile: Chile\n- extranjero: Extranjero', max_length=24, verbose_name='Residence place'),
        ),
        migrations.AlterField(
            model_name='person',
            name='transportation_mode',
            field=models.CharField(choices=[('agua', 'Water'), ('aire', 'Air'), ('tierra', 'Land')], help_text='Opciones:\n- agua: Agua\n- aire: Aire\n- tierra: tierra', max_length=8, verbose_name='Transportation mode'),
        ),
        migrations.AlterField(
            model_name='person',
            name='travel_document',
            field=models.CharField(choices=[('RUN', 'RUN'), ('pasaporte', 'Passport'), ('otro', 'Other')], help_text='Opciones:\n- RUN: RUN\n- pasaporte: Pasaporte\n- otro: Otro', max_length=16, verbose_name='Travel document'),
        ),
        migrations.AlterField(
            model_name='person',
            name='visit_subject',
            field=models.CharField(choices=[('turismo', 'Turism'), ('vacaciones', 'Vacations'), ('visita familiares/amigos', 'Visit to family or friend'), ('trabajo', 'Work'), ('negocios', 'Business'), ('other', 'Other')], max_length=128, verbose_name='Visit subject'),
        ),
        migrations.AlterField(
            model_name='place',
            name='address',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='place',
            name='localidad',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Localidad'),
        ),
        migrations.AlterField(
            model_name='place',
            name='place_type',
            field=models.IntegerField(choices=[(1, 'Turistic service'), (2, 'Turist attraction'), (3, 'Turistic information office'), (4, 'Health place'), (5, 'Check point municipal'), (6, 'Sanitary check point'), (7, 'Border crossing')], help_text='Opciones:\n- 1: Servicio turístico\n- 2: Atracción turística\n- 3: Oficina de información turística\n- 4: Posta rural\n- 5: Punto de control municipal\n- 6: Aduana sanitaria\n- 7: Punto fronterizo', verbose_name='Place type'),
        ),
        migrations.AlterField(
            model_name='place',
            name='turistic_info_office_type',
            field=models.CharField(blank=True, choices=[('SERNATUR', 'SERNATUR'), ('MUNICIPAL', 'MUNICIPAL'), ('GREMIO', 'GREMIO')], help_text='Opciones:\n- SERNATUR: SERNATUR\n- MUNICIPAL: MUNICIPAL\n- GREMIO: GREMIO', max_length=16, null=True, verbose_name='Turistic information office type'),
        ),
        migrations.AlterField(
            model_name='place',
            name='zone',
            field=models.CharField(blank=True, max_length=98, null=True, verbose_name='Zone'),
        ),
        migrations.AlterField(
            model_name='underageperson',
            name='gender',
            field=models.CharField(choices=[('Masculino', 'Male'), ('Femenino', 'Female'), ('Otro', 'Other')], help_text='Opciones:\n- Masculino: Masculino\n- Femenino: Femenino\n- Otro: Otro', max_length=24, verbose_name='Gender'),
        ),
        migrations.AlterField(
            model_name='underageperson',
            name='relationship',
            field=models.CharField(choices=[('amigo/a', 'Friend'), ('colega', 'Colegue'), ('cuñado/a', 'Sibling in law'), ('hermano/a', 'sibling'), ('hijo/a', 'Child'), ('nieto/a', 'Grandchild'), ('primo/a', 'Cousin'), ('sobrino/a', 'Nephew'), ('tio/a', 'Uncle/aunt')], help_text='Opciones:\n- amigo/a: Amiga/o\n- colega: Colega\n- cuñado/a: Cuñada/o\n- hermano/a: hermanoa/o\n- hijo/a: Hija/o\n- nieto/a: Nieta/o\n- primo/a: Prima/o\n- sobrino/a: Sobrina/o\n- tio/a: Tía/Tío\n* Tambien puede ser llenado con una entrada personalizada', max_length=24, verbose_name='Contact replationship'),
        ),
    ]
