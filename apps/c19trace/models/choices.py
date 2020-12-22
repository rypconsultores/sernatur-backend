from django.utils.translation import gettext_lazy as gettext

relationships = (
    ("familiar/amigo", gettext("Family/Friend")),
    ("travel agency", gettext("Travel Agency")),
    ("tour operator", gettext("Tour Operator")),
    ("empresa (negocios o trabajo)", gettext("Company (Business or Work)")),
    ("ninguno", gettext("None")),
)

underage_relationships = (
    ("amigo/a", gettext("Friend")),
    ("colega", gettext("Colegue")),
    ("cuñado/a", gettext("Sibling in law")),
    ("hermano/a", gettext("sibling")),
    ("hijo/a", gettext("Child")),
    ("nieto/a", gettext("Grandchild")),
    ("primo/a", gettext("Cousin")),
    ("sobrino/a", gettext("Nephew")),
    ("tio/a", gettext("Uncle/aunt")),
)

transportation_modes = (
    ('agua', gettext("Water")),
    ('aire', gettext("Air")),
    ('tierra', gettext("Land")),
)

genders = (
    ("Masculino", gettext("Male")),
    ("Femenino", gettext("Female")),
    ("Otro", gettext("Other"))
)

travel_documents = (
    ("RUN", gettext("RUN")),
    ("pasaporte", gettext("Passport")),
    ("otro", gettext("Other"))
)

residence_choices = (
    ('Chile', gettext("Chile")),
    ('extranjero', gettext("Not Chile"))
)

transportation_means = (
    ("Motocicleta", gettext("Motorcycle")),
    ("Bicicleta", gettext("Bycicle")),
    ("Auto/Jeep/Camioneta", gettext("Car/Jeep/Pickup truck")),
    ("Motorhome/Casa Rodante", gettext("Motorhome")),
    ("Bus", gettext("Bus")),
    ("Camión", gettext("Truck"))
)

entry_point_types = (
    ('maritimo', gettext("Maritime")),
    ('aereo', gettext("Aereal")),
    ('terrestre', gettext("Ground")),
)

travel_subject = (
    ('turismo', gettext("Turism")),
    ('vacaciones', gettext('Vacations')),
    ('visita familiares/amigos', gettext('Visit to family or friend')),
    ('trabajo', gettext('Work')),
    ('negocios', gettext('Business')),
    ('other', gettext('Other'))
)
