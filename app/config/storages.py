from storages.backends.s3boto3 import S3Boto3Storage


class S3IdeaStorage(S3Boto3Storage):
    location = 'media'
    default_acl = 'private'
