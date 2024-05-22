from django.core.files.storage import FileSystemStorage

class TemporaryFileSystemStorage(FileSystemStorage):
    def __init__(self, *args, **kwargs):
        kwargs['location'] = '/tmp/media'
        super().__init__(*args, **kwargs)
