from .base import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from dotenv import load_dotenv


load_dotenv()

SECRET_KEY = os.getenv('DJANGO_KEY')
DEBUG = False
ALLOWED_HOSTS = ['167.99.142.3']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql', # we use the postgresql adaptator
        'NAME': os.getenv('POSTGRESQL_DB_NAME'),
        'USER': os.getenv('POSTGRESQL_USER'),
        'PASSWORD': os.getenv('POSTGRESQL_PSWD'),
        'HOST': '',
        'PORT': '5432',
    }
}

sentry_sdk.init(
    dsn="https://59c55e9d23fa4ac3b15a871c4329d542@o622128.ingest.sentry.io/5752572",
    integrations=[DjangoIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,

    # By default the SDK will try to use the SENTRY_RELEASE
    # environment variable, or infer a git commit
    # SHA as release, however you may want to set
    # something more human-readable.
    # release="myapp@1.0.0",
)