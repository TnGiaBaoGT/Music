from django.contrib import admin

# Register your models here.
from .models import Music, User, Purchase, Singer, Vote, Transaction, Album, Like, MusicBundle,BundlePurchase,Listen,MusicCart,MusicPurchased,ComposerEarnings,ComposerEarningsDetail,Ads,Report,BankAccount

class MusicDisplay(admin.ModelAdmin):
    list_display = ('name_music','price_music','status_music','isFree','genre_music','music','upload_date')
admin.site.register(Music,MusicDisplay)
class UserDisplay(admin.ModelAdmin):
    list_display = ('name_user','email_user','phone_user','status_user')
admin.site.register(User,UserDisplay)
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
class MusicPurchaseDisplay(admin.ModelAdmin):
    list_display = ('id_music_purchased','user','purchase_date','momo_token')
admin.site.register(MusicPurchased,MusicPurchaseDisplay)
admin.site.register(ComposerEarnings)
class ComposerEarningsDetailDisplay(admin.ModelAdmin):
    list_display = ('composer_earnings','earnings','purchase_count','view_count','total_earnings','bank_account','withdrawal_date','status_state')
admin.site.register(ComposerEarningsDetail,ComposerEarningsDetailDisplay)
admin.site.register(Ads)
admin.site.register(Report)
class BankAccountDisplay(admin.ModelAdmin):
    list_display = ('user','account_number','bank_name','account_holder_name','expiry_date')
admin.site.register(BankAccount,BankAccountDisplay)
