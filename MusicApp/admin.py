from django.contrib import admin

# Register your models here.
from .models import Music, User, Purchase, Singer, Vote, Transaction, Album, Like

admin.site.register(Music)
admin.site.register(User)
admin.site.register(Purchase)
admin.site.register(Singer)
admin.site.register(Vote)
admin.site.register(Transaction)
admin.site.register(Album)
admin.site.register(Like)
