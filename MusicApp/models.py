from django.db import models
from cloudinary_storage.storage import RawMediaCloudinaryStorage
from django.utils import timezone
from datetime import timedelta

class User (models.Model):
    id_user = models.AutoField(primary_key=True)
    name_user = models.CharField(max_length=200)
    email_user = models.EmailField(max_length=50)
    pass_user = models.CharField(max_length=200)
    phone_user = models.CharField(max_length=20)
    status_user = models.BooleanField(default= True)
    def __str__(self):
        return f"ID: {self.id_user} { ''*20} | Name: {self.name_user}"


    ROLE_CHOICES = [
        ('USER', 'User'),
        ('COMPOSER', 'Composer'),
    ]

    name_role = models.CharField(max_length=100, choices=ROLE_CHOICES,default='User')


class Music (models.Model):
    id_music = models.AutoField(primary_key=True)
    name_music = models.CharField(max_length=200)
    music = models.FileField(upload_to='music_files/',storage=RawMediaCloudinaryStorage())
    name_singer_music = models.CharField(max_length=200)
    release_year_music = models.CharField(max_length=10)
    status_music = models.BooleanField(default= False)
    isFree = models.BooleanField(default= False)
    GENRE_CHOICES = [
        ('POP', 'Pop'),
        ('ROCK', 'Rock'),
        ('JAZZ', 'Jazz'),
        ('CLASSICAL', 'Classical'),
        ('HIPHOP', 'Hip-Hop'),
        ('REMIX', 'Remix'),
        ('ROMANCE', 'Romance'),
        ('BOLERO', 'Bolero'),
    ]

    genre_music = models.CharField(max_length=100, choices=GENRE_CHOICES, default='Pop')
    image_music = models.ImageField(upload_to='music_images/', null=True, blank=True, storage=RawMediaCloudinaryStorage())
    num_vote = models.PositiveIntegerField(default=0)
    composer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, limit_choices_to={'name_role': 'COMPOSER'}, related_name='music_composed')
    listen_count = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name_music

class Listen(models.Model):
    music = models.ForeignKey(Music, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    listened_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user} listened to {self.music}"



class Singer (models.Model):
    id_singer = models.AutoField(primary_key=True)
    name_singer = models.CharField(max_length=200)
    phone_singer = models.CharField(max_length=20)
    email_singer = models.EmailField(max_length=50)
    GENRE_CHOICES = [
        ('POP', 'Pop'),
        ('ROCK', 'Rock'),
        ('JAZZ', 'Jazz'),
        ('CLASSICAL', 'Classical'),
        ('HIPHOP', 'Hip-Hop'),
        ('REMIX', 'Remix'),
        ('ROMANCE', 'Romance'),
        ('BOLERO', 'Bolero'),
    ]
    genre_singer = models.CharField(max_length=50, choices= GENRE_CHOICES,default='Pop')
    sex_singer = models.CharField(max_length=50) 
    image_singer = models.ImageField(upload_to='singer_images/', null=True, blank=True, storage=RawMediaCloudinaryStorage())

    def __str__(self):
        return self.name_singer



class Vote (models.Model):
    id_vote = models.AutoField(primary_key=True)
    comment_vote = models.CharField(max_length=50, null= True)
    report_vote = models.CharField(max_length=50,  null= True, blank= True)
    
    def __str__(self):
        return f"Vote {self.id_vote}"

    user_id_vote = models.ForeignKey(User, on_delete=models.CASCADE, null= True)
    music_id_vote = models.ForeignKey(Music, on_delete=models.CASCADE, null= True)
    
    @property
    def user_name(self):
        return self.user_id_vote.name_user if self.user_id_vote else 'Anonymous'


class Album (models.Model):
    id_album = models.AutoField(primary_key=True)
    name_album = models.CharField(max_length=50)
    
    
    def __str__(self):
        return self.name_album

    music_id_album = models.ManyToManyField(Music, blank=True)
    user_id_album = models.ForeignKey(User, on_delete=models.CASCADE, null= True)
    
    @property
    def music_info(self):
        return [
            {
                'name_music': music.name_music,
                'music': music.music.url if music.music else None,
                'name_singer_music': music.name_singer_music,
                'image_music': music.image_music.url if music.image_music else None,
            }
            for music in self.music_id_album.all()
        ]


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    music = models.ForeignKey(Music, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'music')

    def __str__(self):
        return f"{self.user.name_user} likes {self.music.name_music}"

class Transaction(models.Model):
    id_tran = models.AutoField(primary_key=True)
    user_id_tran = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    total_price_tran = models.FloatField(default=0)
    purchase_date = models.DateTimeField(default=timezone.now)
    is_bundle = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Transaction {self.id_tran} | User: {self.user_id_tran.name_user} | Total Price: {self.total_price_tran}"
    

class MusicBundle(models.Model):
    id_bundle = models.AutoField(primary_key=True)
    name_bundle = models.CharField(max_length=200)
    description_bundle = models.TextField()
    price_bundle = models.FloatField(default=0)
    music_tracks = models.ManyToManyField(Music)
    is_free = models.BooleanField(default=False)  # Indicates if the bundle is free
    access_duration_days = models.IntegerField(default=30)  # Access duration in days
    
    def __str__(self):
        return f"Bundle {self.name_bundle} | Price: {self.price_bundle}"
    def formatted_price(self):
        return "{:,.0f} VND".format(self.price_bundle)
    formatted_price.short_description = 'Price (VND)'

class BundlePurchase(models.Model):
    id_bundle_purchase = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bundle = models.ForeignKey(MusicBundle, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    momo_token = models.CharField(max_length=255, null=True, blank=True)
    
    def is_access_valid(self):
        return self.purchase_date + timedelta(days=self.bundle.access_duration_days) > timezone.now()

    def get_days_left(self):
        expiration_date = self.purchase_date + timedelta(days=self.bundle.access_duration_days)
        remaining_time = expiration_date - timezone.now()
        return max(remaining_time.days, 0)  # Return 0 if the access has expired
    
    def __str__(self):
        return f"Bundle Purchase {self.id_bundle_purchase} | User: {self.user.name_user} | Bundle: {self.bundle.name_bundle}"

class Purchase(models.Model):
    id_purchase = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    bundle = models.ForeignKey(MusicBundle, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    momo_token = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        user_name = self.user.name_user if self.user else "Unknown User"
        bundle_name = self.bundle.name_bundle if self.bundle else "Unknown Bundle"
        return f"Purchase {self.id_purchase} | User: {user_name} | Bundle: {bundle_name}"

    

