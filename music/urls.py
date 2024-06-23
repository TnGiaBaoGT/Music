"""
URL configuration for music project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from MusicApp import views

from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('admin/')),

    path('musics/', views.musicApi),
    path('music/', views.musicApiHTML, name='index'),
    path('musics/<int:id_music>', views.musicApi),
    path('musics/composer/<int:id_user>', views.musicApi),

    path('users/', views.userApi),
    path('users/<int:id_user>', views.userApi),

    path('singers/', views.singerApi),
    path('singers/<int:id_singer>', views.singerApi),

    path('votes/', views.voteApi),
    path('votes/<int:id_vote>', views.voteApi),

    path('transactions/', views.transactionApi),
    path('transactions/<int:id_transaction>', views.transactionApi),
    
    path('albums/', views.albumApi),
    path('albums/<int:id_album>', views.albumApi),
    path('albums/user/<int:id_user>', views.albumApi),

    path('purchases/', views.purchaseApi),
    path('purchases/<int:id_purchase>', views.purchaseApi),
    path('purchases/user/<int:id_user>', views.purchaseApi),

    path('likes/', views.likeApi),
    path('likes/<int:id_like>', views.likeApi),
    path('likes/user/<int:id_user>', views.likeApi),

    path('music/<int:music_id>/like/', views.like_music),
    path('music/<int:music_id>/unlike/', views.unlike_music),

    path('musicbundles/', views.musicbundleApi),
    path('musicbundles/<int:id_musicbundle>/', views.musicbundleApi),

    path('bundlepurchase/', views.bundlepurchaseApi),
    path('bundlepurchase/<int:id_bundlepurchase>/', views.bundlepurchaseApi),
    path('bundlepurchase/user/<int:id_user>/', views.bundlepurchaseApi),

    path('confirm-purchase/<int:id_purchase>/', views.confirm_purchase),
    path('receive_momo_token/', views.receive_momo_token),
    
    path('listen/<int:id_music>', views.listen_song),

    path('musiccart/', views.musiccartApi),
    path('musiccart/<int:id_cart>/', views.musiccartApi),
    path('musiccart/user/<int:id_user>/', views.musiccartApi),

    path('musicpurchased/', views.musicpurchasedApi),
    path('musicpurchased/<int:id_music_purchased>/', views.musicpurchasedApi),
    path('musicpurchased/user/<int:id_user>/', views.musicpurchasedApi),

    path('confirm-music-purchase/', views.confirm_music_purchase),
    path('receive_momo_token_music/', views.receive_momo_token_music),
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
