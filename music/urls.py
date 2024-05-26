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
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
