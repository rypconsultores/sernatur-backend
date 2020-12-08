from datetime import datetime, timedelta
from hashlib import sha512
from uuid import uuid4, uuid1

from django.conf import settings

import pytz
from django.utils.translation import gettext_lazy as gettext


def thenow() -> datetime:
    return datetime.now().astimezone(pytz.utc)


def choices_to_helptext(choices, title=gettext("Options")):
    return f'{title}:\n' + '\n'.join(
        f"- {v}: {l}"
        for v, l in choices
    )


def password_request_expiracy() -> datetime:
    return (
        datetime.now(tz=pytz.utc)
        + timedelta(**settings.USER_PASSWORD_REQUEST_EXPIRES)
    )


def password_request_id() -> str:
    return uuid1().hex + uuid4().hex


def password_request_key() -> str:
    return  sha512((uuid4().hex + uuid4().hex).encode()).hexdigest()
