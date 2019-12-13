from settings import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'ACTUAL_VALUE'),
        'USER': os.environ.get('DB_USER', 'ACTUAL_VALUE'),
        'PASSWORD': os.environ.get('DB_PASS', 'ACTUAL_VALUE'),
        'HOST': os.environ.get('DB_HOST', 'ACTUAL_VALUE'),
        'PORT': os.environ.get('DB_PORT', 'ACTUAL_VALUE_PROBABLY_5432'),
    }
}
