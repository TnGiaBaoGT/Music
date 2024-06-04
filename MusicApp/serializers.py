from rest_framework import serializers
from MusicApp.models import Music, User, Singer, Vote, Transaction, Album, Purchase, Like

class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = '__all__'

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

class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'
