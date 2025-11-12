from pathlib import Path
from typing import Any, Dict, List, Tuple

from decouple import config
from django.urls import reverse_lazy
from django.utils.functional import Promise

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
    "apps.catalog",
    "apps.pages",
    "apps.vacancies",
    "apps.core",
    "apps.accounts",
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
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
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

TIME_ZONE: str = "Europe/Moscow"
USE_I18N: bool = True
USE_TZ: bool = True

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

STATIC_URL: str = "static/"
STATICFILES_DIRS: List[Any] = [
    BASE_DIR / "static",
]
STATIC_ROOT: Path = BASE_DIR / "staticfiles"

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

LOGIN_URL: Promise = reverse_lazy("accounts:signin")
LOGIN_REDIRECT_URL: Promise = reverse_lazy("catalog:product_list")
LOGOUT_REDIRECT_URL: Promise = LOGIN_URL
