import os

DATABASE_ENGINE = 'sqlite3'
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = [
    'django.contrib.sessions',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'lazy_tags',
    'tests',
]

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
]

PROJECT_ROOT = os.path.dirname(__file__)
ROOT_URLCONF = 'tests.urls'

SITE_ID = 1

SECRET_KEY = 'something-something'

ROOT_URLCONF = 'tests.urls'

STATIC_URL = '/site_media/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, "test_static")

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

# Required in Django>=1.10.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            # ... some options here ...
        },
    },
]
