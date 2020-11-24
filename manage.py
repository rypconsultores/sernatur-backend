#!/usr/bin/env python
import os
import sys
from dotenv import load_dotenv

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.env.default")

    if (
        not os.getenv("DJANGO_DOTENV_LOADED", None) and
        os.path.exists(os.path.join(os.path.dirname(__file__), ".env"))
    ):
        os.environ["DJANGO_DOTENV_LOADED"] = "yes"
        sys.stderr.write("Using .env file\n")
        load_dotenv(verbose=True)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn'_ import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)
