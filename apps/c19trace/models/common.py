from django.utils.translation import gettext_lazy as gettext

relationships = (
    ("abuelo/a", gettext("Grandparent")),
    ("amigo/a", gettext("Friend")),
    ("colega", gettext("Colegue")),
    ("cuñado/a", gettext("Sibling in law")),
    ("hermano/a", gettext("sibling")),
    ("hijo/a", gettext("Child")),
    ("nieto/a", gettext("Grandchild")),
    ("padre/madre", gettext("Parent")),
    ("primo/a", gettext("Cousin")),
    ("sobrino/a", gettext("Nephew")),
    ("suegro/a", gettext("Parent in law")),
    ("tio/a", gettext("Uncle/aunt")),
)

underage_relationships = (
    ("amigo/a", gettext("Friend")),
    ("colega", gettext("Colegue")),
    ("cuñado/a", gettext("Sibling in law")),
    ("hermano/a", gettext("sibling")),
    ("hijo/a", gettext("Child")),
    ("nieto/a", gettext("Grandchild")),
    ("primo/a", gettext("Cousin")),
    ("sobrino/a", gettext("Nephew"))
)

transportation_modes = (
    ('agua', gettext("water")),
    ('aire', gettext("air")),
    ('tierra', gettext("Land")),
)

genders = (
    ("Masculino", gettext("Male")),
    ("Femenino", gettext("Female")),
    ("Otro", gettext("Other"))
)
