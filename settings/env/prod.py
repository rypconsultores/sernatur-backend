from ..main import *

# Production configuration
DEBUG = False

# Database - # AVOID THIS! Try dotenv URL schema
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': '',
#         'USER': '',
#         'PASS': '',
#         'HOST': '',
#     }
# }

# Static file hash
STATICFILES_STORAGE = (
    "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
)
