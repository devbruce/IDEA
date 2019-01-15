from .base import *

DEBUG = True

INSTALLED_APPS.append('django_extensions')

secrets = json.load(open(os.path.join(SECRETS_DIR, 'dev.json')))
ALLOWED_HOSTS = secrets['ALLOWED_HOSTS']
DATABASES = secrets['DATABASES']

DEFAULT_FILE_STORAGE = 'config.storages.S3IdeaStorage'
AWS_ACCESS_KEY_ID = secrets['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = secrets['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = secrets['AWS_STORAGE_BUCKET_NAME']
AWS_S3_REGION_NAME = 'ap-northeast-2'
