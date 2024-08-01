from django.contrib import admin

# Register your models here.
from .models import Music, User, Purchase, Singer, Vote, Transaction, Album, Like, MusicBundle,BundlePurchase,Listen,MusicCart,MusicPurchased,ComposerEarnings,ComposerEarningsDetail,Ads,Report,BankAccount

admin.site.register(Music)
admin.site.register(User)
admin.site.register(Purchase)
admin.site.register(Singer)
admin.site.register(Vote)
admin.site.register(Transaction)
admin.site.register(Album)
admin.site.register(Like)
admin.site.register(MusicBundle)
class BundlePurchaseAdmin(admin.ModelAdmin):
    list_display = ('id_bundle_purchase', 'user', 'bundle', 'purchase_date', 'days_left')

    def days_left(self, obj):
        return obj.get_days_left()
    days_left.short_description = 'Days Left'
admin.site.register(BundlePurchase, BundlePurchaseAdmin)
admin.site.register(Listen)
admin.site.register(MusicCart)
admin.site.register(MusicPurchased)
admin.site.register(ComposerEarnings)
admin.site.register(ComposerEarningsDetail)
admin.site.register(Ads)
admin.site.register(Report)
class BankAccountDisplay(admin.ModelAdmin):
    list_display = ('user','account_number','bank_name','account_holder_name','expiry_date')
admin.site.register(BankAccount,BankAccountDisplay)
