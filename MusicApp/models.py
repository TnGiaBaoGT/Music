from django.db import models
from cloudinary_storage.storage import RawMediaCloudinaryStorage

class Music (models.Model):
    id_music = models.AutoField(primary_key=True)
    name_music = models.CharField(max_length=200)
    music = models.FileField(upload_to='music_files/',storage=RawMediaCloudinaryStorage())
    name_singer_music = models.CharField(max_length=200)
    release_year_music = models.CharField(max_length=10)
    price_music = models.FloatField(default=0)
    status_music = models.BooleanField(default= False)
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
    
    def __str__(self):
        return self.name_music
    
    







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




class Singer (models.Model):
    id_singer = models.AutoField(primary_key=True)
    name_singer = models.CharField(max_length=200)
    phone_singer = models.CharField(max_length=20)
    email_singer = models.EmailField(max_length=50)
    genre_singer = models.CharField(max_length=50)
    sex_singer = models.CharField(max_length=50) 

    def __str__(self):
        return self.name_singer




class Vote (models.Model):
    id_vote = models.AutoField(primary_key=True)
    comment_vote = models.CharField(max_length=50)
    report_vote = models.CharField(max_length=50)
    num_vote = models.IntegerField()
    
    def __str__(self):
        return f"Vote {self.id_vote}"

    user_id_vote = models.ForeignKey(User, on_delete=models.CASCADE, null= True)
    music_id_vote = models.ForeignKey(Music, on_delete=models.CASCADE, null= True)



class Transaction (models.Model):
    id_tran = models.AutoField(primary_key=True)
    price_tran = models.FloatField(default=0)
    type_tran = models.CharField(max_length=50)
    def __str__(self):
        return f"Transaction {self.id_tran}"

    user_id_tran = models.ForeignKey(User, on_delete=models.CASCADE, null= True)



class Album (models.Model):
    id_album = models.AutoField(primary_key=True)
    name_album = models.CharField(max_length=50)
    
    
    def __str__(self):
        return self.name_album

    music_id_album = models.ManyToManyField(Music)
    user_id_album = models.ForeignKey(User, on_delete=models.CASCADE, null= True)
