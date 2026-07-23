"""
==========================================================
Nexora Web
Professional Django Settings
Version : 2.0
==========================================================
"""

from pathlib import Path
import os

# ==========================================================
# BASE DIRECTORY
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================================================
# ENVIRONMENT
# ==========================================================

ENVIRONMENT = os.environ.get(
    "DJANGO_ENV",
    "development",
)

DEBUG = os.environ.get(
    "DJANGO_DEBUG",
    "True",
).lower() == "true"

# ==========================================================
# SECRET KEY
# ==========================================================

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "CHANGE-THIS-IN-PRODUCTION-VERY-LONG-RANDOM-KEY",
)

# ==========================================================
# PROJECT INFORMATION
# ==========================================================

PROJECT_NAME = "Nexora Web"

PROJECT_VERSION = "2.0.0"

PROJECT_COMPANY = "Nexora Holding"

PROJECT_DESCRIPTION = (
    "Professional Website Design & Development Platform"
)

PROJECT_EMAIL = "info@nexoraweb.com"

PROJECT_PHONE = "+98 900 000 0000"

PROJECT_WEBSITE = "https://nexoraweb.com"

# ==========================================================
# DOMAIN
# ==========================================================

DOMAIN = os.environ.get(
    "DOMAIN",
    "nexoraweb.pythonanywhere.com",
)

SITE_URL = f"https://{DOMAIN}"

# ==========================================================
# ALLOWED HOSTS
# ==========================================================

ALLOWED_HOSTS = [

    "127.0.0.1",

    "localhost",

    DOMAIN,

]

# ==========================================================
# TRUSTED ORIGINS
# ==========================================================

CSRF_TRUSTED_ORIGINS = [

    f"https://{DOMAIN}",

]

# ==========================================================
# SECURITY BASE
# ==========================================================

if not DEBUG:

    SECURE_SSL_REDIRECT = True

    SESSION_COOKIE_SECURE = True

    CSRF_COOKIE_SECURE = True

    SECURE_HSTS_SECONDS = 31536000

    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

    SECURE_HSTS_PRELOAD = True

else:

    SECURE_SSL_REDIRECT = False

    SESSION_COOKIE_SECURE = False

    CSRF_COOKIE_SECURE = False

# ==========================================================
# COOKIE SECURITY
# ==========================================================

SESSION_COOKIE_HTTPONLY = True

CSRF_COOKIE_HTTPONLY = True

SESSION_COOKIE_SAMESITE = "Lax"

CSRF_COOKIE_SAMESITE = "Lax"

SESSION_COOKIE_AGE = 60 * 60 * 24 * 30

SESSION_SAVE_EVERY_REQUEST = True

SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# ==========================================================
# INSTALLED APPLICATIONS
# ==========================================================

DJANGO_APPS = [

    "jazzmin",

    "django.contrib.admin",

    "django.contrib.auth",

    "django.contrib.contenttypes",

    "django.contrib.sessions",

    "django.contrib.messages",

    "django.contrib.staticfiles",

    "django.contrib.sites",

    "django.contrib.humanize",

    "django.contrib.sitemaps",

]

# ==========================================================
# THIRD PARTY APPS
# ==========================================================

THIRD_PARTY_APPS = [

    "csp",
    "axes",
    "django_ratelimit",
    # Future Security
    # "axes",
    # "csp",
    # "django_otp",
    # "two_factor",

]

# ==========================================================
# LOCAL APPS
# ==========================================================

LOCAL_APPS = [

    "core",

    "accounts",

]

# ==========================================================
# FINAL INSTALLED APPS
# ==========================================================

INSTALLED_APPS = (

    DJANGO_APPS

    + THIRD_PARTY_APPS

    + LOCAL_APPS

)

# ==========================================================
# SITE ID
# ==========================================================

SITE_ID = 1

# ==========================================================
# INTERNATIONALIZATION
# ==========================================================

LANGUAGE_CODE = "fa"

TIME_ZONE = "Asia/Tehran"

USE_I18N = True

USE_TZ = True

# ==========================================================
# SUPPORTED LANGUAGES
# ==========================================================

LANGUAGES = [

    ("fa", "Persian"),

    ("en", "English"),

]

# ==========================================================
# LOCALE PATH
# ==========================================================

LOCALE_PATHS = [

    BASE_DIR / "locale",

]

# ==========================================================
# DEFAULT AUTO FIELD
# ==========================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ==========================================================
# MIDDLEWARE
# ==========================================================

MIDDLEWARE = [

    # ------------------------------------------------------
    # SECURITY
    # ------------------------------------------------------

    "django.middleware.security.SecurityMiddleware",

    # WhiteNoise
    "whitenoise.middleware.WhiteNoiseMiddleware",

    # ------------------------------------------------------
    # SESSION
    # ------------------------------------------------------

    "django.contrib.sessions.middleware.SessionMiddleware",

    # ------------------------------------------------------
    # LANGUAGE
    # ------------------------------------------------------

    "django.middleware.locale.LocaleMiddleware",

    # ------------------------------------------------------
    # COMMON
    # ------------------------------------------------------

    "django.middleware.common.CommonMiddleware",

    # ------------------------------------------------------
    # CSRF
    # ------------------------------------------------------

    "axes.middleware.AxesMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",

    # ------------------------------------------------------
    # AUTHENTICATION
    # ------------------------------------------------------

    "django.contrib.auth.middleware.AuthenticationMiddleware",

    # ------------------------------------------------------
    # MESSAGES
    # ------------------------------------------------------

    "django.contrib.messages.middleware.MessageMiddleware",

    # ------------------------------------------------------
    # CLICKJACKING
    # ------------------------------------------------------

    "csp.middleware.CSPMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",

]

# ==========================================================
# ROOT URL
# ==========================================================

ROOT_URLCONF = "service_site.urls"

# ==========================================================
# WSGI
# ==========================================================

WSGI_APPLICATION = "service_site.wsgi.application"

# ==========================================================
# ASGI
# ==========================================================

ASGI_APPLICATION = "service_site.asgi.application"

# ==========================================================
# TEMPLATES
# ==========================================================

TEMPLATES = [

    {

        "BACKEND": "django.template.backends.django.DjangoTemplates",

        # --------------------------------------------------
        # Global Templates Folder
        # --------------------------------------------------

        "DIRS": [

            BASE_DIR / "templates",

        ],

        "APP_DIRS": True,

        "OPTIONS": {

            "context_processors": [

                # ------------------------------------------
                # Django Default
                # ------------------------------------------

                "django.template.context_processors.debug",

                "django.template.context_processors.request",

                "django.contrib.auth.context_processors.auth",

                "django.contrib.messages.context_processors.messages",

                "django.template.context_processors.i18n",

                "django.template.context_processors.media",

                "django.template.context_processors.static",

                # ------------------------------------------
                # Custom Context
                # ------------------------------------------

                "core.context_processors.global_data",

            ],

        },

    },

]

# ==========================================================
# TEMPLATE OPTIONS
# ==========================================================

FORM_RENDERER = "django.forms.renderers.DjangoTemplates"

# ==========================================================
# MESSAGE FRAMEWORK
# ==========================================================

from django.contrib.messages import constants as messages

MESSAGE_TAGS = {

    messages.DEBUG: "secondary",

    messages.INFO: "info",

    messages.SUCCESS: "success",

    messages.WARNING: "warning",

    messages.ERROR: "danger",

}

# ==========================================================
# DATABASE
# ==========================================================

DATABASE_ENGINE = os.environ.get(
    "DATABASE_ENGINE",
    "sqlite",
)

# ==========================================================
# SQLITE
# ==========================================================

if DATABASE_ENGINE == "sqlite":

    DATABASES = {

        "default": {

            "ENGINE": "django.db.backends.sqlite3",

            "NAME": BASE_DIR / "db.sqlite3",

        }

    }

# ==========================================================
# POSTGRESQL
# ==========================================================

elif DATABASE_ENGINE == "postgres":

    DATABASES = {

        "default": {

            "ENGINE": "django.db.backends.postgresql",

            "NAME": os.environ.get("POSTGRES_DB"),

            "USER": os.environ.get("POSTGRES_USER"),

            "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),

            "HOST": os.environ.get("POSTGRES_HOST"),

            "PORT": os.environ.get("POSTGRES_PORT", "5432"),

            "CONN_MAX_AGE": 600,

            "OPTIONS": {

                "connect_timeout": 10,

            },

        }

    }

# ==========================================================
# MYSQL
# ==========================================================

elif DATABASE_ENGINE == "mysql":

    DATABASES = {

        "default": {

            "ENGINE": "django.db.backends.mysql",

            "NAME": os.environ.get("MYSQL_DATABASE"),

            "USER": os.environ.get("MYSQL_USER"),

            "PASSWORD": os.environ.get("MYSQL_PASSWORD"),

            "HOST": os.environ.get("MYSQL_HOST"),

            "PORT": os.environ.get("MYSQL_PORT", "3306"),

            "CONN_MAX_AGE": 600,

        }

    }

# ==========================================================
# DATABASE OPTIONS
# ==========================================================

DATABASE_ROUTERS = []

DEFAULT_DB_ALIAS = "default"

# ==========================================================
# AUTHENTICATION
# ==========================================================

AUTHENTICATION_BACKENDS = [

    "django.contrib.auth.backends.ModelBackend",

]

# ==========================================================
# PASSWORD HASHERS
# ==========================================================

PASSWORD_HASHERS = [

    # Strongest (Recommended)
    "django.contrib.auth.hashers.Argon2PasswordHasher",

    # Backup
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",

    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",

    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",

]

# ==========================================================
# PASSWORD VALIDATORS
# ==========================================================

AUTH_PASSWORD_VALIDATORS = [

    {

        "NAME":
        "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",

    },

    {

        "NAME":
        "django.contrib.auth.password_validation.MinimumLengthValidator",

        "OPTIONS": {

            "min_length": 12,

        }

    },

    {

        "NAME":
        "django.contrib.auth.password_validation.CommonPasswordValidator",

    },

    {

        "NAME":
        "django.contrib.auth.password_validation.NumericPasswordValidator",

    },

]

# ==========================================================
# LOGIN
# ==========================================================

LOGIN_URL = "login"

LOGIN_REDIRECT_URL = "core:dashboard"

LOGOUT_REDIRECT_URL = "core:home"

# ==========================================================
# SESSION
# ==========================================================

SESSION_ENGINE = "django.contrib.sessions.backends.db"

SESSION_COOKIE_NAME = "nexora_session"

SESSION_SAVE_EVERY_REQUEST = True

SESSION_COOKIE_AGE = 60 * 60 * 24 * 30

SESSION_EXPIRE_AT_BROWSER_CLOSE = False

SESSION_COOKIE_HTTPONLY = True

SESSION_COOKIE_SAMESITE = "Lax"

# ==========================================================
# CSRF
# ==========================================================

CSRF_COOKIE_NAME = "nexora_csrf"

CSRF_COOKIE_HTTPONLY = True

CSRF_COOKIE_SAMESITE = "Lax"

# ==========================================================
# SECURITY LIMITS
# ==========================================================

DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760

FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760

DATA_UPLOAD_MAX_NUMBER_FIELDS = 5000

# ==========================================================
# STATIC FILES
# ==========================================================

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [

    BASE_DIR / "static",

]

STATICFILES_STORAGE = (

    "whitenoise.storage.CompressedManifestStaticFilesStorage"

)

# ==========================================================
# MEDIA FILES
# ==========================================================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"

# ==========================================================
# FILE UPLOAD
# ==========================================================

FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755

FILE_UPLOAD_PERMISSIONS = 0o644

FILE_UPLOAD_HANDLERS = [

    "django.core.files.uploadhandler.MemoryFileUploadHandler",

    "django.core.files.uploadhandler.TemporaryFileUploadHandler",

]

# ==========================================================
# STATIC FINDERS
# ==========================================================

STATICFILES_FINDERS = [

    "django.contrib.staticfiles.finders.FileSystemFinder",

    "django.contrib.staticfiles.finders.AppDirectoriesFinder",

]

# ==========================================================
# WHITENOISE
# ==========================================================

WHITENOISE_KEEP_ONLY_HASHED_FILES = True

WHITENOISE_AUTOREFRESH = DEBUG

WHITENOISE_USE_FINDERS = DEBUG

WHITENOISE_MAX_AGE = 31536000

# ==========================================================
# CACHE CONTROL
# ==========================================================

if not DEBUG:

    SECURE_PROXY_SSL_HEADER = (

        "HTTP_X_FORWARDED_PROTO",

        "https",

    )

# ==========================================================
# EMAIL CONFIGURATION
# ==========================================================

EMAIL_BACKEND = os.environ.get(
    "EMAIL_BACKEND",
    "django.core.mail.backends.smtp.EmailBackend",
)

EMAIL_HOST = os.environ.get(
    "EMAIL_HOST",
    "smtp.gmail.com",
)

EMAIL_PORT = int(
    os.environ.get(
        "EMAIL_PORT",
        "587",
    )
)

EMAIL_USE_TLS = True

EMAIL_USE_SSL = False

EMAIL_HOST_USER = os.environ.get(
    "EMAIL_HOST_USER",
    "",
)

EMAIL_HOST_PASSWORD = os.environ.get(
    "EMAIL_HOST_PASSWORD",
    "",
)

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

SERVER_EMAIL = EMAIL_HOST_USER

# ==========================================================
# ADMINS
# ==========================================================

ADMINS = [

    (

        "Nexora Admin",

        "admin@nexoraweb.com",

    ),

]

MANAGERS = ADMINS

# ==========================================================
# LOGGING
# ==========================================================

LOGGING = {

    "version": 1,

    "disable_existing_loggers": False,

    "formatters": {

        "verbose": {

            "format": (
                "{levelname} "
                "{asctime} "
                "{module} "
                "{message}"
            ),

            "style": "{",

        },

        "simple": {

            "format": "{levelname} {message}",

            "style": "{",

        },

    },

    "handlers": {

        "console": {

            "class": "logging.StreamHandler",

            "formatter": "simple",

        },

        "file": {

            "class": "logging.FileHandler",

            "filename": BASE_DIR / "logs" / "django.log",

            "formatter": "verbose",

        },

    },

    "loggers": {

        "django": {

            "handlers": [

                "console",

                "file",

            ],

            "level": "INFO",

            "propagate": True,

        },

    },

}

# ==========================================================
# CACHE
# ==========================================================

CACHE_TIMEOUT = 60 * 15

CACHES = {

    "default": {

        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",

        "LOCATION": "nexora-cache",

        "TIMEOUT": CACHE_TIMEOUT,

        "OPTIONS": {

            "MAX_ENTRIES": 10000,

        },

    }

}

# ==========================================================
# CACHE MIDDLEWARE
# ==========================================================

CACHE_MIDDLEWARE_ALIAS = "default"

CACHE_MIDDLEWARE_SECONDS = CACHE_TIMEOUT

CACHE_MIDDLEWARE_KEY_PREFIX = "nexora"

# ==========================================================
# SESSION CACHE
# ==========================================================

SESSION_CACHE_ALIAS = "default"

# ==========================================================
# TEMPLATE CACHE
# ==========================================================

USE_ETAGS = True

# ==========================================================
# BROWSER CACHE
# ==========================================================

if not DEBUG:

    SECURE_BROWSER_XSS_FILTER = True

    SECURE_CONTENT_TYPE_NOSNIFF = True

# ==========================================================
# SECURITY HEADERS
# ==========================================================

SECURE_CONTENT_TYPE_NOSNIFF = True

X_FRAME_OPTIONS = "DENY"

SECURE_REFERRER_POLICY = "same-origin"

SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"

SECURE_CROSS_ORIGIN_EMBEDDER_POLICY = "require-corp"

SECURE_CROSS_ORIGIN_RESOURCE_POLICY = "same-origin"

# ==========================================================
# HTTPS
# ==========================================================

if not DEBUG:

    SECURE_SSL_REDIRECT = True

    SECURE_PROXY_SSL_HEADER = (

        "HTTP_X_FORWARDED_PROTO",

        "https",

    )

# ==========================================================
# XSS
# ==========================================================

SECURE_BROWSER_XSS_FILTER = True

# ==========================================================
# MIME
# ==========================================================

SECURE_CONTENT_TYPE_NOSNIFF = True

# ==========================================================
# UPLOAD SECURITY
# ==========================================================

# Maximum upload size (50 MB)
DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800

FILE_UPLOAD_MAX_MEMORY_SIZE = 52428800

# Maximum POST fields
DATA_UPLOAD_MAX_NUMBER_FIELDS = 5000

# Upload permissions
FILE_UPLOAD_PERMISSIONS = 0o644

FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755

# Temporary upload directory
FILE_UPLOAD_TEMP_DIR = BASE_DIR / "tmp"

# ==========================================================
# FILE SECURITY
# ==========================================================

# Prevent serving unknown files
FILE_CHARSET = "utf-8"

DEFAULT_CHARSET = "utf-8"

# ==========================================================
# IMAGE SECURITY
# ==========================================================

IMAGE_UPLOAD_MAX_PIXELS = None

# ==========================================================
# PERFORMANCE
# ==========================================================

USE_ETAGS = True

APPEND_SLASH = True

PREPEND_WWW = False

# ==========================================================
# HTTP
# ==========================================================

USE_X_FORWARDED_HOST = True

USE_X_FORWARDED_PORT = True

# ==========================================================
# RESPONSE
# ==========================================================

DEFAULT_CONTENT_TYPE = "text/html"

DEFAULT_EXCEPTION_REPORTER = (
    "django.views.debug.ExceptionReporter"
)

# ==========================================================
# REQUEST LIMITS
# ==========================================================

CSRF_FAILURE_VIEW = (
    "django.views.csrf.csrf_failure"
)

# ==========================================================
# TIMEOUTS
# ==========================================================

SESSION_COOKIE_AGE = 60 * 60 * 24 * 30

SESSION_SAVE_EVERY_REQUEST = True

# ==========================================================
# CONTENT SECURITY POLICY (django-csp 4.x)
# ==========================================================

CONTENT_SECURITY_POLICY = {
    "DIRECTIVES": {
        "default-src": ("'self'",),

        "script-src": (
            "'self'",
            "'unsafe-inline'",
            "https://cdn.jsdelivr.net",
        ),

        "style-src": (
            "'self'",
            "'unsafe-inline'",
            "https://cdn.jsdelivr.net",
            "https://fonts.googleapis.com",
        ),

        "font-src": (
            "'self'",
            "https://fonts.gstatic.com",
            "data:",
        ),

        "img-src": (
            "'self'",
            "data:",
            "blob:",
        ),

        "connect-src": (
            "'self'",
        ),

        "object-src": (
            "'none'",
        ),

        "base-uri": (
            "'self'",
        ),

        "form-action": (
            "'self'",
        ),

        "frame-ancestors": (
            "'none'",
        ),

        "media-src": (
            "'self'",
        ),

        "worker-src": (
            "'self'",
            "blob:",
        ),
    }
}

# ==========================================================
# PERMISSIONS POLICY
# ==========================================================

SECURE_PERMISSIONS_POLICY = {
    "accelerometer": [],
    "autoplay": [],
    "camera": [],
    "display-capture": [],
    "encrypted-media": [],
    "fullscreen": ["self"],
    "geolocation": [],
    "gyroscope": [],
    "magnetometer": [],
    "microphone": [],
    "midi": [],
    "payment": [],
    "picture-in-picture": [],
    "usb": [],
}

# ==========================================================
# DJANGO AXES (Brute Force Protection)
# ==========================================================

AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesStandaloneBackend",
    "django.contrib.auth.backends.ModelBackend",
]

AXES_ENABLED = True

AXES_FAILURE_LIMIT = 5

AXES_COOLOFF_TIME = 1  # ساعت

AXES_LOCKOUT_CALLABLE = None

AXES_RESET_ON_SUCCESS = True
