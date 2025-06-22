import logging.config
import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "django-insecure-(r85c*cj)9n+z%r^m6j8)nozrw7$*b*@^v=!$@9k6p3x9bhmto")

DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

INSTALLED_APPS = [
  "django.contrib.admin",
  "django.contrib.auth",
  "django.contrib.contenttypes",
  "django.contrib.sessions",
  "django.contrib.messages",
  "django.contrib.staticfiles",
  "rest_framework",
  "rest_framework_simplejwt",
]

MIDDLEWARE = [
  "django.middleware.security.SecurityMiddleware",
  "django.contrib.sessions.middleware.SessionMiddleware",
  "django.middleware.common.CommonMiddleware",
  "django.middleware.csrf.CsrfViewMiddleware",
  "django.contrib.auth.middleware.AuthenticationMiddleware",
  "django.contrib.messages.middleware.MessageMiddleware",
  "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "{{ project_name }}.urls"

TEMPLATES = [
  {
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [os.path.join(BASE_DIR, "templates")],
    "APP_DIRS": True,
    "OPTIONS": {
      "context_processors": [
        "django.template.context_processors.debug",
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
      ],
    },
  },
]

WSGI_APPLICATION = "{{ project_name }}.wsgi.application"

DB_ENGINE = os.getenv("DB_ENGINE", "sqlite")
if DB_ENGINE == "postgresql":
  DATABASES = {
    "default": {
      "ENGINE": "django.db.backends.postgresql",
      "NAME": os.getenv("DB_NAME", "postgres"),
      "USER": os.getenv("DB_USER", "postgres"),
      "PASSWORD": os.getenv("DB_PASSWORD", "postgres"),
      "HOST": os.getenv("DB_HOST", "db"),
      "PORT": os.getenv("DB_PORT", "5432"),
    }
  }
elif DB_ENGINE == "sqlite":
  DATABASES = {
    "default": {
      "ENGINE": "django.db.backends.sqlite3",
      "NAME": BASE_DIR / "db.sqlite3",
    }
  }
else:
  raise ValueError(f"The DB_ENGINE value '{DB_ENGINE}' in .env is not supported. Use 'sqlite' or 'postgresql'.")

AUTH_PASSWORD_VALIDATORS = [
  {
    "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
  },
  {
    "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
  },
  {
    "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
  },
  {
    "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
  },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = "media/"

MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
  "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
  "DEFAULT_AUTHENTICATION_CLASSES": [
    "rest_framework.authentication.SessionAuthentication",
    "rest_framework.authentication.BasicAuthentication",
    "rest_framework_simplejwt.authentication.JWTAuthentication",
  ],
  "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"],
  "DEFAULT_RENDERER_CLASSES": [
    "rest_framework.renderers.JSONRenderer",
    "rest_framework.renderers.BrowsableAPIRenderer",
  ],
  "DEFAULT_PARSER_CLASSES": [
    "rest_framework.parsers.JSONParser",
    "rest_framework.parsers.FormParser",
    "rest_framework.parsers.MultiPartParser",
  ],
  "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
  "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
  "PAGE_SIZE": 10,
}

SIMPLE_JWT = {
  "ACCESS_TOKEN_LIFETIME": timedelta(minutes=int(os.getenv("JWT_ACCESS_TOKEN_LIFETIME_MINUTES", 60))),
  "REFRESH_TOKEN_LIFETIME": timedelta(days=int(os.getenv("JWT_REFRESH_TOKEN_LIFETIME_DAYS", 7))),
  "ROTATE_REFRESH_TOKENS": os.getenv("JWT_ROTATE_REFRESH_TOKENS", "False").lower() == "true",
  "BLACKLIST_AFTER_ROTATION": os.getenv("JWT_BLACKLIST_AFTER_ROTATION", "True").lower() == "true",
  "UPDATE_LAST_LOGIN": os.getenv("JWT_UPDATE_LAST_LOGIN", "False").lower() == "true",
  "ALGORITHM": os.getenv("JWT_ALGORITHM", "HS256"),
  "SIGNING_KEY": os.getenv("JWT_SIGNING_KEY", "your-super-secret-key-that-you-must-change-in-prod"),
  "USER_ID_FIELD": os.getenv("JWT_USER_ID_FIELD", "id"),
  "USER_ID_CLAIM": os.getenv("JWT_USER_ID_CLAIM", "user_id"),
  "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
}

CACHES = {
  "default": {
    "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    "LOCATION": "unique-snowflake",
  }
}

LOGGING_CONFIG = None
LOGLEVEL = os.getenv("LOG_LEVEL", "info").upper()
logging.config.dictConfig(
  {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
      "verbose": {
        "format": "%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(module)s %(process)d %(thread)d %(message)s",
        "datefmt": "%d-%m-%Y %I:%M %p",
      },
      "simple": {
        "format": "{levelname} {message}",
        "style": "{",
      },
    },
    "handlers": {
      "email_file": {
        "level": "INFO",
        "class": "logging.handlers.RotatingFileHandler",
        "filename": os.path.join(BASE_DIR, "logs/email_service.log"),
        "maxBytes": 1024 * 1024 * 5,  # 5 MB
        "backupCount": 5,
        "formatter": "verbose",
      },
      "email_errors": {
        "level": "ERROR",
        "class": "logging.handlers.RotatingFileHandler",
        "filename": os.path.join(BASE_DIR, "logs/email_errors.log"),
        "maxBytes": 1024 * 1024 * 5,  # 5 MB
        "backupCount": 5,
        "formatter": "verbose",
      },
      "console": {
        "level": "DEBUG",
        "class": "logging.StreamHandler",
        "formatter": "simple",
      },
    },
    "loggers": {
      "": {
        "level": LOGLEVEL,
        "propagate": True,
        "handlers": ["email_file", "email_errors", "console"],
      },
    },
  }
)
