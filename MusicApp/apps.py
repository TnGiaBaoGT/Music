from django.apps import AppConfig
import os

class MusicappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MusicApp'
def ready(self):
        # Ensure the /tmp/media directory and subdirectories exist
        os.makedirs('/tmp/media/music_files', exist_ok=True)
        os.makedirs('/tmp/media/music_images', exist_ok=True)
 
