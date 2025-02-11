from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-bf7o_41ju6#f-lwii$+xsh5pts2zwq55tbp6&of8&2pv0ivx$%"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS += [
    "debug_toolbar",
]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INTERNAL_IPS = [
    "127.0.0.1",
]

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
