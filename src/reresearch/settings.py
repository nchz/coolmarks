from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


DEBUG = True
SECRET_KEY = "($39x(vd=1$1uc%nzq7!xrd*$uz0+0v*qsy2+3&oc&9#8q@^k3"
ALLOWED_HOSTS = ["*"]


STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "collectstatic"
# STATICFILES_DIRS = [BASE_DIR / "static"]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # dependencies
    "rest_framework",
    # project apps
    "apps.loader",
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

SITE_ID = 1
ROOT_URLCONF = "reresearch.urls"
WSGI_APPLICATION = "reresearch.wsgi.application"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "data" / "db.sqlite3",
    }
}


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
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


_VALIDATORS_PREFIX = "django.contrib.auth.password_validation"
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": f"{_VALIDATORS_PREFIX}.UserAttributeSimilarityValidator"},
    # {"NAME": f"{_VALIDATORS_PREFIX}.MinimumLengthValidator"},
    # {"NAME": f"{_VALIDATORS_PREFIX}.CommonPasswordValidator"},
    {"NAME": f"{_VALIDATORS_PREFIX}.NumericPasswordValidator"},
]


LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 100,
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
        "rest_framework.renderers.TemplateHTMLRenderer",
    ],
}
