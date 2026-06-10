from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from decouple import Csv, config
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django_stubs_ext import StrOrPromise

BASE_DIR: Path = Path(__file__).resolve().parent.parent

SECRET_KEY: str = config("DJANGO_SECRET_KEY")

DEBUG: bool = config("DJANGO_DEBUG", default=False, cast=bool)

ALLOWED_HOSTS: List[str] = config(
    "DJANGO_ALLOWED_HOSTS",
    default="127.0.0.1,localhost",
    cast=Csv(),
)

CSRF_TRUSTED_ORIGINS: List[str] = config(
    "DJANGO_CSRF_TRUSTED_ORIGINS",
    default="",
    cast=Csv(),
)

CSRF_COOKIE_SECURE: bool = config(
    "DJANGO_CSRF_COOKIE_SECURE",
    default=False,
    cast=bool,
)

SESSION_COOKIE_SECURE: bool = config(
    "DJANGO_SESSION_COOKIE_SECURE",
    default=False,
    cast=bool,
)

SECURE_PROXY_SSL_HEADER: Tuple[str, str] = (
    "HTTP_X_FORWARDED_PROTO",
    "https",
)

SECURE_CROSS_ORIGIN_OPENER_POLICY: Optional[str] = (
    config(
        "DJANGO_SECURE_CROSS_ORIGIN_OPENER_POLICY",
        default="",
    )
    or None
)

INTERNAL_IPS: List[str] = [
    "127.0.0.1",
]

INSTALLED_APPS: List[str] = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    "unfold.contrib.import_export",
    "unfold.contrib.guardian",
    "unfold.contrib.simple_history",
    "unfold.contrib.location_field",
    "unfold.contrib.constance",
    "modeltranslation",
    "django.contrib.admin",
    "django.contrib.admindocs",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "phonenumber_field",
    "django_resized",
    "django_cleanup.apps.CleanupConfig",
    "django_user_agents",
    "health_check",
    "compressor",
    "django_filters",
    "spurl",
    "django_htmx",
    "social_django",
    "apps.core",
    "apps.carts",
    "apps.catalog",
    "apps.pages",
    "apps.accounts",
    "apps.promotions",
    "apps.orders",
    "apps.reviews",
    "apps.favorites",
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
    "csp.middleware.CSPMiddleware",
    "django_user_agents.middleware.UserAgentMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]

if DEBUG:
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")

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
                "apps.carts.context_processors.cart",
                "apps.favorites.context_processors.favorite",
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
    },
    "ratelimit": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": config(
            "RATELIMIT_CACHE_LOCATION", default="redis://127.0.0.1:6379/2"
        ),
    },
}

RATELIMIT_USE_CACHE: str = "ratelimit"

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

AUTHENTICATION_BACKENDS: List[str] = [
    "social_core.backends.google.GoogleOAuth2",
    "django.contrib.auth.backends.ModelBackend",
]

SOCIAL_AUTH_IMMUTABLE_USER_FIELDS: List[str] = [
    "first_name",
    "last_name",
    "email",
]
SOCIAL_AUTH_JSONFIELD_ENABLED: bool = True
SOCIAL_AUTH_URL_NAMESPACE: str = "accounts:social"
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY: str = config("GOOGLE_OAUTH2_CLIENT_ID")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET: str = config("GOOGLE_OAUTH2_CLIENT_SECRET")
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE: List[str] = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]
SOCIAL_AUTH_PIPELINE: List[str] = [
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.user.get_username",
    "apps.accounts.pipelines.associate_by_email",
    "social_core.pipeline.user.create_user",
    "apps.accounts.pipelines.activate_user",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
    "apps.accounts.pipelines.send_signin_social_notification",
]
SOCIAL_AUTH_LOGIN_ERROR_URL: StrOrPromise = reverse_lazy(
    viewname="accounts:signin"
)

TIME_ZONE: str = "Europe/Moscow"
USE_I18N: bool = True
USE_TZ: bool = True

CELERY_BROKER_URL = config(
    "CELERY_BROKER_URL", default="redis://127.0.0.1:6379/1"
)
CELERY_RESULT_BACKEND = config(
    "CELERY_BROKER_URL", default="redis://127.0.0.1:6379/1"
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

MEDIA_URL: str = "/media/"
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
        "img-src": ["'self'", "data:"],
        "script-src": [
            "'self'",
            "https://smartcaptcha.cloud.yandex.ru",
            "https://captcha-api.yandex.ru",
            "https://suggest-maps.yandex.ru/v1/suggest",
        ],
        "style-src": [
            "'self'",
            "https://fonts.googleapis.com",
            "'unsafe-inline'",
        ],
        "connect-src": ["'self'", "https://suggest-maps.yandex.ru/v1/suggest"],
        "form-action": ["'self'"],
        "frame-ancestors": ["'none'"],
        "base-uri": ["'self'"],
        "object-src": ["'none'"],
        "frame-src": [
            "https://yandex.ru/map-widget/",
            "https://smartcaptcha.cloud.yandex.ru",
            "https://captcha-api.yandex.ru",
        ],
    },
}

if config(
    "DJANGO_CSP_UPGRADE_INSECURE_REQUESTS",
    default=False,
    cast=bool,
):
    CONTENT_SECURITY_POLICY["DIRECTIVES"]["upgrade-insecure-requests"] = []

LOGIN_URL: StrOrPromise = reverse_lazy(viewname="accounts:signin")
LOGIN_REDIRECT_URL: StrOrPromise = reverse_lazy(viewname="pages:home")
LOGOUT_REDIRECT_URL: StrOrPromise = LOGIN_URL

UNFOLD: Dict[str, Any] = {
    "SITE_TITLE": "Марлин",
    "SITE_HEADER": "Марлин",
    "SITE_URL": reverse_lazy(viewname="pages:home"),
    "DASHBOARD_CALLBACK": (
        "apps.core.admins.admin_dashboard.dashboard_callback"
    ),
    "SITE_ICON": {
        "light": lambda request: static("img/logo.png"),
        "dark": lambda request: static("img/logo.png"),
    },
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/svg+xml",
            "href": lambda request: static("img/favicon.ico"),
        },
    ],
    "SHOW_BACK_BUTTON": True,
    "ENVIRONMENT": lambda request: [
        ("DEVELOPMENT" if DEBUG else "PRODUCTION"),
        ("info" if DEBUG else "danger"),
    ],
    "SHOW_LANGUAGES": True,
    "EXTENSIONS": {
        "modeltranslation": {
            "flags": {
                "en": "🇬🇧",
                "ru": "🇷🇺",
            },
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": _("Infrastructure"),
                "separator": True,
                "items": [
                    {
                        "title": "Celery Flower",
                        "icon": "auto_graph",
                        "link": "http://localhost:5555",
                        "permission": (
                            lambda request: request.user.is_superuser
                        ),
                    },
                    {
                        "title": "Health Check",
                        "icon": "health_and_safety",
                        "link": reverse_lazy(viewname="health-check"),
                        "permission": (
                            lambda request: request.user.is_superuser
                        ),
                    },
                ],
            },
            {
                "title": _("Catalog"),
                "separator": True,
                "items": [
                    {
                        "title": _("Products"),
                        "icon": "inventory_2",
                        "link": reverse_lazy(
                            "admin:catalog_product_changelist"
                        ),
                    },
                    {
                        "title": _("Categories"),
                        "icon": "account_tree",
                        "link": reverse_lazy(
                            "admin:catalog_category_changelist"
                        ),
                    },
                    {
                        "title": _("Favorites"),
                        "icon": "favorite",
                        "link": reverse_lazy(
                            "admin:favorites_favorite_changelist"
                        ),
                    },
                    {
                        "title": _("Reviews"),
                        "icon": "star",
                        "link": reverse_lazy(
                            "admin:reviews_productreview_changelist"
                        ),
                    },
                ],
            },
            {
                "title": _("Users & Access"),
                "separator": True,
                "items": [
                    {
                        "title": _("Users"),
                        "icon": "person",
                        "link": reverse_lazy("admin:accounts_user_changelist"),
                    },
                    {
                        "title": _("Social accounts"),
                        "icon": "passkey",
                        "link": reverse_lazy(
                            "admin:accounts_proxyusersocialauth_changelist"
                        ),
                    },
                    {
                        "title": _("Groups"),
                        "icon": "group",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                ],
            },
            {
                "title": _("Orders & Carts"),
                "separator": True,
                "items": [
                    {
                        "title": _("Orders"),
                        "icon": "receipt_long",
                        "link": reverse_lazy("admin:orders_order_changelist"),
                    },
                    {
                        "title": _("Order items"),
                        "icon": "format_list_bulleted",
                        "link": reverse_lazy(
                            "admin:orders_orderitem_changelist"
                        ),
                    },
                    {
                        "title": _("Carts"),
                        "icon": "shopping_cart",
                        "link": reverse_lazy("admin:carts_cart_changelist"),
                    },
                    {
                        "title": _("Cart Items"),
                        "icon": "list_alt",
                        "link": reverse_lazy(
                            "admin:carts_cartitem_changelist"
                        ),
                    },
                ],
            },
        ],
    },
}

YANDEX_SMART_CAPTCHA_VALIDATE_URL: str = (
    "https://smartcaptcha.yandexcloud.net/validate"
)
YANDEX_SMART_CAPTCHA_CLIENT_KEY: str = config(
    "YANDEX_SMART_CAPTCHA_CLIENT_KEY"
)
YANDEX_SMART_CAPTCHA_SERVER_KEY: str = config(
    "YANDEX_SMART_CAPTCHA_SERVER_KEY"
)
YANDEX_GEOSUGGEST_KEY: str = config("YANDEX_GEOSUGGEST_KEY")
