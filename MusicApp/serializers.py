from rest_framework import serializers
from MusicApp.models import Music, User, Singer, Vote, Transaction, Album, Purchase, Like, MusicBundle, BundlePurchase,MusicCart,MusicPurchased,MusicPurchasedItem,ComposerEarnings,ComposerEarningsDetail,Ads,Report,BankAccount
from datetime import timedelta
from django.utils import timezone

class MusicSerializer(serializers.ModelSerializer):
    formatted_price = serializers.SerializerMethodField()
    class Meta:
        model = Music
        fields = '__all__'
    def get_formatted_price(self, obj):
        return "{:,.0f} VND".format(obj.price_music)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class SingerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Singer
        fields = '__all__'


class VoteSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user_id_vote.name_user')
    class Meta:
        model = Vote
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class AlbumSerializer(serializers.ModelSerializer):
    music_info = serializers.SerializerMethodField()
    class Meta:
        model = Album
        fields = '__all__'

    def get_music_info(self, obj):
        return obj.music_info


class LikeSerializer(serializers.ModelSerializer):
    music_info = serializers.SerializerMethodField() 
    class Meta:
        model = Like
        fields = '__all__'
    def get_music_info(self, obj):
        music = obj.music
        return {
            'name_music': music.name_music,
            'music_url': music.music.url if music.music else None,
            'name_singer_music': music.name_singer_music,
            'image_music': music.image_music.url if music.image_music else None
        }

class MusicBundleSerializer(serializers.ModelSerializer):
    formatted_price = serializers.SerializerMethodField()
    class Meta:
        model = MusicBundle
        fields = '__all__'
        
    def get_formatted_price(self, obj):
        return "{:,.0f} VND".format(obj.price_bundle)

class BundlePurchaseSerializer(serializers.ModelSerializer):
    days_left = serializers.SerializerMethodField()
    bundle = MusicBundleSerializer()
    class Meta:
        model = BundlePurchase
        fields = '__all__'
        
    def get_days_left(self, obj):
        expiration_date = obj.purchase_date + timedelta(days=obj.bundle.access_duration_days)
        remaining_time = expiration_date - timezone.now()
        return max(remaining_time.days, 0)  # Return 0 if the access has expired

class PurchaseSerializer(serializers.ModelSerializer):
    bundle_info = MusicBundleSerializer(source='bundle', read_only=True)
    class Meta:
        model = Purchase
        fields = '__all__'


class MusicCartSerializer(serializers.ModelSerializer):
    music_info = MusicSerializer(source='music',read_only=True)
    class Meta:
        model = MusicCart
        fields = '__all__'


class MusicPurchasedItemSerializer(serializers.ModelSerializer):
    music = MusicSerializer()  # Use MusicSerializer to serialize each MusicPurchasedItem

    class Meta:
        model = MusicPurchasedItem
        fields = ['music']

class MusicPurchasedSerializer(serializers.ModelSerializer):
    music_items = MusicPurchasedItemSerializer(source='musicpurchaseditem_set', many=True)
    class Meta:
        model = MusicPurchased
        fields = '__all__'

class ComposerEarningsSerializer(serializers.ModelSerializer):
    music_track = MusicSerializer(source="music",read_only=True)
    class Meta:
        model = ComposerEarnings
        fields = '__all__'

class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = '__all__'

class ComposerEarningsDetailSerializer(serializers.ModelSerializer):
    composer_earnings_detail = ComposerEarningsSerializer(source="composer_earnings",read_only=True)
    bank_info = BankAccountSerializer(source="bank_account")
    class Meta:
        model = ComposerEarningsDetail
        fields = '__all__'

class AdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ads
        fields = '__all__'

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'

