import os

from django.conf import settings


def pytest_configure():
  if not settings.configured:
    settings.configure(
      INSTALLED_APPS=[
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "rest_framework",
        "src.shared.infrastructure.api",
      ],
      SECRET_KEY="a-very-secret-key-for-tests",
      DATABASES={
        "default": {
          "ENGINE": "django.db.backends.sqlite3",
          "NAME": ":memory:",
        }
      },
      REST_FRAMEWORK={
        "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
        "DEFAULT_PARSER_CLASSES": ("rest_framework.parsers.JSONParser",),
      },
    )
  os.environ.setdefault("DJANGO_SETTINGS_MODULE", "relancio.settings")
