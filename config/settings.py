from pathlib import Path
from typing import Any, Dict, List, Tuple

from decouple import config
from django.urls import reverse_lazy
from django_stubs_ext import StrOrPromise

BASE_DIR: Path = Path(__file__).resolve().parent.parent

SECRET_KEY: str = config("DJANGO_SECRET_KEY")

DEBUG: bool = config("DJANGO_DEBUG", default=False, cast=bool)

ALLOWED_HOSTS: List[str] = [
    "127.0.0.1",
]

INTERNAL_IPS: List[str] = [
    "127.0.0.1",
]

INSTALLED_APPS: List[str] = [
    "modeltranslation",
    "django.contrib.admin",
    "django.contrib.admindocs",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "debug_toolbar",
    "phonenumber_field",
    "django_user_agents",
    "health_check",
    "compressor",
    "django_filters",
    "spurl",
    "apps.catalog",
    "apps.pages",
    "apps.vacancies",
    "apps.core",
    "apps.accounts",
    "apps.carts",
    "apps.promotions",
]

MIDDLEWARE: List[str] = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "csp.middleware.CSPMiddleware",
    "django_user_agents.middleware.UserAgentMiddleware",
]

ROOT_URLCONF: str = "config.urls"

TEMPLATES: List[Dict[str, Any]] = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION: str = "config.wsgi.application"

DATABASES: Dict[str, Any] = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DATABASE_NAME"),
        "USER": config("DATABASE_USER"),
        "PASSWORD": config("DATABASE_PASSWORD"),
        "HOST": config("DATABASE_HOST", default="127.0.0.1"),
        "PORT": config("DATABASE_PORT", default=5432),
    }
}

CACHES: Dict[str, Any] = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": config(
            "CACHE_LOCATION", default="redis://127.0.0.1:6379/0"
        ),
    }
}

AUTH_PASSWORD_VALIDATORS: List[Dict[str, str]] = [
    {
        "NAME": "django.contrib.auth.password_validation."
        "UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation."
        "MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation."
        "CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation."
        "NumericPasswordValidator",
    },
]

AUTH_USER_MODEL: str = "accounts.User"

TIME_ZONE: str = "Europe/Moscow"
USE_I18N: bool = True
USE_TZ: bool = True

CELERY_BROKER_URL = config("CELERY_URL", default="redis://127.0.0.1:6379/1")
CELERY_RESULT_BACKEND = config(
    "CELERY_URL", default="redis://127.0.0.1:6379/1"
)
CELERY_TIMEZONE: str = TIME_ZONE
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SOFT_TIME_LIMIT: int = 60
CELERY_TASK_TIME_LIMIT: int = 120
CELERY_TASK_ACKS_LATE: bool = True
CELERY_TASK_REJECT_ON_WORKER_LOST: bool = True
CELERY_WORKER_MAX_TASKS_PER_CHILD: int = 1000
CELERY_WORKER_MAX_MEMORY_PER_CHILD: int = 400_000

LANGUAGE_CODE: str = "ru-ru"
MODELTRANSLATION_DEFAULT_LANGUAGE: str = "en"
LANGUAGES: List[Tuple[str, str]] = [
    ("ru", "Русский"),
    ("en", "English"),
]
LANGUAGE_COOKIE_NAME: str = "language"

LOCALE_PATHS: List[Any] = [
    BASE_DIR / "locale",
]

STATIC_URL: str = "/static/"
STATICFILES_DIRS: List[Any] = [
    BASE_DIR / "static",
]
STATIC_ROOT: Path = BASE_DIR / "staticfiles"

STATICFILES_FINDERS: Tuple[str, ...] = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)
COMPRESS_OFFLINE: bool = not DEBUG
COMPRESS_ENABLED: bool = True
COMPRESS_CSS_FILTERS: List[str] = [
    "compressor.filters.cssmin.CSSMinFilter",
]

MEDIA_URL: str = "media/"
MEDIA_ROOT: Path = BASE_DIR / "media"

DEFAULT_AUTO_FIELD: str = "django.db.models.BigAutoField"

FIXTURE_DIRS: List[str] = [
    "fixtures",
]

EMAIL_HOST: str = "smtp.gmail.com"
EMAIL_PORT: int = 587
EMAIL_USE_TLS: bool = True
EMAIL_HOST_USER: str = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD: str = config("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL: str = EMAIL_HOST_USER

CONTENT_SECURITY_POLICY: Dict[str, Any] = {
    "EXCLUDE_URL_PREFIXES": ["/admin"],
    "DIRECTIVES": {
        "default-src": ["'none'"],
        "font-src": ["'self'", "https://fonts.gstatic.com", "data:"],
        "img-src": ["'self'"],
        "script-src": ["'self'"],
        "style-src": ["'self'", "https://fonts.googleapis.com"],
        "connect-src": ["'self'"],
        "form-action": ["'self'"],
        "frame-ancestors": ["'none'"],
        "base-uri": ["'self'"],
        "object-src": ["'none'"],
        "frame-src": ["https://yandex.ru/map-widget/"],
        "upgrade-insecure-requests": [],
    },
}

LOGIN_URL: StrOrPromise = reverse_lazy(viewname="accounts:signin")
LOGIN_REDIRECT_URL: StrOrPromise = reverse_lazy(viewname="pages:home")
LOGOUT_REDIRECT_URL: StrOrPromise = LOGIN_URL
