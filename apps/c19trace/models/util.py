from datetime import datetime

import pytz
from django.utils.translation import gettext_lazy as gettext


def thenow() -> datetime:
    return datetime.now().astimezone(pytz.utc)


def choices_to_helptext(choices, title=gettext("Options")):
    return f'{title}:\n' + '\n'.join(
        f"- {v}: {l}"
        for v, l in choices
    )
