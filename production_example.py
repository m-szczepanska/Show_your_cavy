from settings import *


ALLOWED_HOSTS.append("http://your_public_dns_ipv4,your_public_dns_ipv4")
ALLOWED_HOSTS.append("*")

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
