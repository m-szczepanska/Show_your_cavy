from settings import *


DOMAIN_URL = 'YOUR_DOMAIN_GOES_HERE'

# Yes, the domain name here is repeated twice; Nginx magic
ALLOWED_HOSTS.append(f'http://{DOMAIN_URL},{DOMAIN_URL}')
ALLOWED_HOSTS.append('*')

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

# Always use S3
AWS_DEFAULT_ACL = 'public-read'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = DEFAULT_FILE_STORAGE
AWS_ACCESS_KEY_ID = 'your_access_key_id'
AWS_SECRET_ACCESS_KEY = 'your_secret_access_key'
AWS_STORAGE_BUCKET_NAME = 'squeakoo-static'
