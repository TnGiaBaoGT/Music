from django.db import models
from cloudinary_storage.storage import RawMediaCloudinaryStorage
from django.utils import timezone
from datetime import timedelta
from datetime import datetime

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
    price_music = models.FloatField(default=0)
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
    upload_date = models.DateTimeField(default=datetime.now)
    
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


class Album(models.Model):
    id_album = models.AutoField(primary_key=True)
    name_album = models.CharField(max_length=50)
    music_id_album = models.ManyToManyField(Music, blank=True)
    user_id_album = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name_album

    @property
    def music_info(self):
        return [
            {
                'name_music': music.name_music,
                'music': music.music.url if music.music else None,
                'name_singer_music': music.name_singer_music,
                'image_music': music.image_music.url if music.image_music else None,
                'genre_music': music.genre_music,
                'listen_count': music.listen_count,
                'num_vote': music.num_vote,
                'isFree': music.isFree,
                'status_music': music.status_music,
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

class MusicCart(models.Model):
    id_cart = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    music = models.ForeignKey(Music, on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    momo_token = models.CharField(max_length=255,null=True,blank=True)
    
    def __str__(self):
        user_name = self.user.name_user if self.user else "Unknown User"
        music_name = self.music.name_music if self.music else "Unknown Music Name"
        return f"User: {user_name} purchase {music_name}"

class MusicPurchased(models.Model):
    id_music_purchased = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    # music = models.ManyToManyField(Music, through='MusicPurchasedItem')
    purchase_date = models.DateTimeField(auto_now_add=True)
    momo_token = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Music Purchase {self.id_music_purchased} | User: {self.user.name_user} "

class MusicPurchasedItem(models.Model):
    music_purchased = models.ForeignKey(MusicPurchased, on_delete=models.CASCADE)
    music = models.ForeignKey(Music, on_delete=models.CASCADE)

class ComposerEarnings(models.Model):
    composer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'name_role': 'COMPOSER'})
    month = models.DateField()  # No default value
    earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    purchase_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)  # New field for view count
    music = models.ForeignKey(Music, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Composer: {self.composer.name_user} | Month: {self.month.strftime('%Y-%m')} | Earnings: {self.earnings}"

    @classmethod
    def create_for_music_upload(cls, music):
        # Create ComposerEarnings for the month of music upload
        cls.objects.create(
            composer=music.composer,
            month=music.upload_date,  # Use upload date of the music, set day to 1
            earnings=0,
            purchase_count=0,
            view_count=0,
            music=music
        )

class ComposerEarningsDetail(models.Model):
    composer_earnings = models.OneToOneField(ComposerEarnings, on_delete=models.CASCADE)
    momo_token = models.CharField(max_length=255, null=True, blank=True)
    earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    purchase_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calculate_total_earnings(self):
        self.total_earnings = self.earnings + (self.view_count * 50)
        self.save()

    def __str__(self):
        return f"Composer: {self.composer_earnings.composer.name_user} | Total Earnings: {self.total_earnings}"

class Ads (models.Model):
    id_ads = models.AutoField(primary_key=True)
    name_ads = models.CharField(max_length=255)
    description_ads = models.CharField(max_length=255)
    image_ads = models.ImageField(upload_to='ads_image/',storage=RawMediaCloudinaryStorage())
    view_count = models.IntegerField(default=0)
    price_ads = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    total_earnings_ads = models.DecimalField(max_digits=10,decimal_places=2,default=0)


    def calculate_total_earnings_ads(self):
        self.total_earnings_ads = self.price_ads * self.view_count
        self.save()

    def increment_view_count(self):
        self.view_count += 1
        self.calculate_total_earnings_ads()

    def __str__(self):
        return f"Views: {self.view_count} | Price: {self.price_ads} | Total Earnings:{self.total_earnings_ads}"
    

class Report(models.Model):
    id_report = models.AutoField(primary_key=True)
    
    REPORT_CHOICES = [
        ('COPYRIGHT_INFRINGEMENT', 'Vi phạm bản quyền'),
        ('PLAGIARISM', 'Đạo nhạc'),
        ('UNAUTHORIZED_SAMPLING', 'Sử dụng trái phép mẫu âm thanh'),
        ('UNAUTHORIZED_COVER', 'Cover không được phép'),
        ('UNAUTHORIZED_PUBLIC_PERFORMANCE', 'Biểu diễn công khai không được phép'),
        ('UNAUTHORIZED_DISTRIBUTION', 'Phân phối không được phép'),
    ]
    
    report_choice = models.CharField(max_length=50, choices=REPORT_CHOICES, default='COPYRIGHT_INFRINGEMENT')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    music = models.ForeignKey(Music, on_delete=models.CASCADE)
    report_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User: {self.user.name_user} | Music: {self.music.name_music} | Report: {self.report_choice}"
