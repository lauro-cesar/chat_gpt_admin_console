"""
"""
from celery.schedules import crontab
import os
import firebase_admin
from firebase_admin import credentials
from typing import Any, Dict
from django.utils.translation import gettext as _, gettext_lazy as l_
import tiktoken
import openai


# First Run, just for downlaod encoding



# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUTH_USER_MODEL = "accounts.Account"
LOGIN_URL = "/web-api/v1/accounts/login/"
LOGIN_REDIRECT_URL = "/console/manager/"

DEBUG = int(os.environ.get("DEBUG", default=0))


APP_NAME = os.environ.get("APP_NAME", "TEMPLATE PROJECT (edit in settings or set ENV APP_NAME variable)")
SITE_HEADER = l_(f"{APP_NAME} API Console")
SITE_TITLE = l_(f"{APP_NAME} Console")
SITE_INDEX_TITLE = l_(f"{APP_NAME} Console")

DEFAULT_APP_ORDER_VALUE = 1000
DEFAULT_MODEL_ORDER_VALUE = 1000
#every account type below or equal this level is considered SUPER_USER
SUPER_USER_MAX_LEVEL=10
OPERATOR_USER_MAX_LEVEL=100


SITES_APP_LIST_ORDER_VALUE = 2000
FLATPAGES_APP_LIST_ORDER_VALUE = 3000
AUTH_APP_LIST_ORDER_VALUE = 5000


NGINX_DOCKER_HTTP_PORT = os.environ.get("NGINX_DOCKER_HTTP_PORT", default="9056")

API_BASE_URI = os.environ.get("API_BASE_URI", default=f"console.gamerstash.app")

WEB_API_ADDRESS = os.environ.get("WEB_API_ADDRESS", default=f"https://{API_BASE_URI}")
REST_API_ADDRESS = os.environ.get("REST_API_ADDRESS", default=f"https://{API_BASE_URI}")
SOCKET_API_ADDRESS = os.environ.get(
    "SOCKET_API_ADDRESS", default=f"wss://{API_BASE_URI}"
)

if os.path.exists(f"{BASE_DIR}/project/service-account-file.json"):
    FIREBASE_CERTIFICATE = credentials.Certificate(
        f"{BASE_DIR}/project/service-account-file.json"
    )
    FIREBASE_APP = firebase_admin.initialize_app(FIREBASE_CERTIFICATE)

ALL_MODELS = []

FQDNS = os.environ.get(f"FQDNS", default="localhost,{API_BASE_URI}")
DATABASE_HOST = (os.environ.get("DATABASE_HOST", default="127.0.0.1"),)

DATABASE_ENGINE= os.environ.get(
            "DATABASE_ENGINE", default="django.db.backends.postgresql"
        ),


#OpenAI Index settings
REDIS_VECTOR_DB_HOST=  os.environ.get("REDIS_VECTOR_DB_HOST", default="project_redis_vector_db") 
REDIS_VECTOR_DB_PORT=  os.environ.get("REDIS_VECTOR_DB_PORT", default=6379)
REDIS_VECTOR_DB_PASSWORD= os.environ.get("REDIS_VECTOR_DB_PASSWORD", default="")
VECTOR_DB_VECTOR_DIM =  1536
VECTOR_DB_VECTOR_NUMBER = 1000                
VECTOR_DB_INDEX_NAME = "embeddings-index"           
VECTOR_DB_HNSW_INDEX_NAME = f"{VECTOR_DB_INDEX_NAME}_HNSW"
VECTOR_DB_PREFIX = "doc"                            
VECTOR_DB_DISTANCE_METRIC = "COSINE"



REDIS_CACHE_HOST = os.environ.get("REDIS_CACHE_HOST", default="localhost")
REDIS_CACHE_PORT = os.environ.get("REDIS_CACHE_PORT", default=6379)
REDIS_CACHE_DB = os.environ.get("REDIS_CACHE_DB", default=0)

REDIS_CHANNELS_HOST = os.environ.get("REDIS_CHANNELS_HOST", default="localhost")
REDIS_CHANNELS_PORT = os.environ.get("REDIS_CHANNELS_PORT", default=6379)
REDIS_CHANNELS_DB = os.environ.get("REDIS_CHANNELS_DB", default=0)

REDIS_QUEUE_HOST = os.environ.get("REDIS_QUEUE_HOST", default="localhost")
REDIS_QUEUE_PORT = os.environ.get("REDIS_QUEUE_PORT", default=6379)
REDIS_QUEUE_DB = os.environ.get("REDIS_QUEUE_DB", default=0)


REDIS_QUEUE_QUEUE_NAME = os.environ.get(
    "REDIS_QUEUE_QUEUE_NAME", default="default_django_queue"
)

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    default="_fake_key_",
)
SRID = 4674


NOTIFICATIONS_BASE_SITE = f"{API_BASE_URI}"

TEST = False

CELERY_BROKER_URL = f"redis://{REDIS_QUEUE_HOST}:{REDIS_QUEUE_PORT}"
CELERY_RESULT_BACKEND = f"redis://{REDIS_QUEUE_HOST}:{REDIS_QUEUE_PORT}"
CELERY_TASK_DEFAULT_QUEUE = REDIS_QUEUE_QUEUE_NAME

CELERY_ENABLE_UTC = False
TIME_ZONE = 'America/Chicago'
CELERY_TIMEZONE = 'America/Chicago'
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SERIALIZER = "json"
TASK_OFFSET_LIMIT = 50


SENDGRID_API_KEY = os.environ.get(
    "SENDGRID_API_KEY",
    default="_fake_key_",
)
EMAIL_BACKEND = (
    "project.custom_backends.send_grid_email_backend.SendGridDjangoEmailBackend"
)
DEFAULT_FROM_EMAIL = "naoresponda@sharedway.app"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework_xml.parsers.XMLParser",
    ],
    # "EXCEPTION_HANDLER": "server.exception_handler.custom_exception_handler",
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_THROTTLE_RATES": {"anon": "1000/day", "user": "500000/day"},
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "project.pagination.FlutterPagination",
    "PAGE_SIZE": 150,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication"
    ],
}

SITE_ID = 1
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

API_VERSION = 1
APPEND_SLASH = True
X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]

#

INSTALLED_APPS = [
    "corsheaders",
    "project_tools.apps.ProjectToolsConfig",
    "accounts.apps.AccountsConfig",
    "project.apps.ProjectConfig",
    "documents.apps.DocumentsConfig",
    "organizations.apps.OrganizationsConfig",
    "chats.apps.ChatsConfig",
    "rest_framework",
    "django_filters",
    "rest_framework.authtoken",
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.flatpages",
    "django.contrib.humanize",
    "channels",
]

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# "project.middleware.ConsoleAuthMiddleWare",

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.contrib.sites.middleware.CurrentSiteMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "project.middleware.RestSSOAuthMiddleWare",
    "project.middleware.SSOAuthMiddleWare",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.flatpages.middleware.FlatpageFallbackMiddleware",
    "django.middleware.cache.FetchFromCacheMiddleware",
]

# CSRF_USE_SESSIONS = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost",
    "http://localhost:9988",
]

CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS

# FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

ROOT_URLCONF = "project.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
            os.path.join(BASE_DIR, "forms/templates"),
            os.path.join(BASE_DIR, "media/private"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
            # "loaders": [
            #     "django.template.loaders.filesystem.Loader",
            #     "django.template.loaders.app_directories.Loader",
            # ],
        },
    }
]

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(REDIS_CHANNELS_HOST, REDIS_CHANNELS_PORT)],
        },
    },
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"redis://{REDIS_CACHE_HOST}:{REDIS_CACHE_PORT}",
        "OPTIONS": {
            "parser_class": "redis.connection.PythonParser",
            "pool_class": "redis.BlockingConnectionPool",
        },
    }
}

WSGI_APPLICATION = "project.wsgi.application"

# django.db.backends.postgresql


DATABASES = {
    "default": {
        "ENGINE": DATABASE_ENGINE,
        "NAME": os.environ.get("DATABASE_NAME", default="django_db"),
        "USER": os.environ.get("DATABASE_USER", default="django_user"),
        "PASSWORD": os.environ.get("DATABASE_PASSWORD", default="django_password"),
        "HOST": os.environ.get("DATABASE_HOST", default="127.0.0.1"),
        "PORT": os.environ.get("DATABASE_PORT", default="5434"),
    }
}

LEAFLET_CONFIG = {
    "DEFAULT_CENTER": (-49, -29),
    "DEFAULT_ZOOM": 4,
    "MAX_ZOOM": 20,
    "MIN_ZOOM": 3,
    "SCALE": "both",
    "ATTRIBUTION_PREFIX": "Inspired by Life in GIS (Lauro Cesar)",
}

# {
#     "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
# },

AUTH_PASSWORD_VALIDATORS = [
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

LANGUAGE_CODE = "en-US"
LANGUAGES = [("en-us", "English")]

USE_I18N = True
USE_THOUSAND_SEPARATOR = True
USE_L10N = True

STATIC_URL = "/static/"
MEDIA_URL = "/media/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

ASSETS_DIR = os.path.join(BASE_DIR, "assets")
PRIVATE_DIR = os.path.join(BASE_DIR, "media/private")
