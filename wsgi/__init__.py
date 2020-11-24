"""
WSGI config for whole project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.env.default")

if (
   not os.getenv("DJANGO_DOTENV_LOADED", None) and
   os.path.exists(os.path.join(os.path.dirname(__file__), "..", ".env"))
):
    os.environ["DJANGO_DOTENV_LOADED"] = "yes"
    sys.stderr.write("Using .env file\n")
    load_dotenv(verbose=True)

application = get_wsgi_application()
