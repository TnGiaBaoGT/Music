from django.contrib import admin

# Register your models here.
from .models import Music, User, Singer, Vote, Transaction, Album

admin.site.register(Music)
admin.site.register(User)
admin.site.register(Singer)
admin.site.register(Vote)
admin.site.register(Transaction)
admin.site.register(Album)
