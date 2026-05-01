from storages.backends.s3boto3 import S3Boto3Storage

class ProxiedMinioStorage(S3Boto3Storage):
    def url(self, name):
        return f"/media/{name}"