from datetime import datetime

import pytz
from django.utils.translation import gettext_lazy as t


def thenow() -> datetime:
    return datetime.now().astimezone(pytz.utc)


def choices_to_helptext(choices, title=t("options")):
    return f'{title}:\n' + '\n'.join(
        f"{v}: {l}"
        for v, l in choices
    )
