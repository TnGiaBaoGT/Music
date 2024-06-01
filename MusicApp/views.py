from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from MusicApp.models import Music, User, Singer, Vote, Transaction, Album
from MusicApp.serializers import MusicSerializer, UserSerializer, SingerSerializer, VoteSerializer, TransactionSerializer, AlbumSerializer
from django.shortcuts import render
@csrf_exempt
def musicApi(request, id_music=0):
    if request.method == 'GET':
        if id_music == 0:
            music = Music.objects.all()
            music_serializer = MusicSerializer(music, many=True)
        else:
            try:
                music = Music.objects.get(id_music=id_music)
                music_serializer = MusicSerializer(music)
            except Music.DoesNotExist:
                return JsonResponse({'mess': 'Record not found'}, status=404)
        return JsonResponse({'music':music_serializer.data}, safe=False)
    
    elif request.method == 'POST':
        music_data = JSONParser().parse(request)
        music_serializer = MusicSerializer(data=music_data)
        if music_serializer.is_valid():
            music_serializer.save()
            return JsonResponse({'mess': 'Added Successfully'}, safe=False)
        return JsonResponse("Failed to Add", safe=False, status=400)
    
    elif request.method == 'PUT':
        music_data = JSONParser().parse(request)
        try:
            music = Music.objects.get(id_music=id_music)
            music_serializer = MusicSerializer(music, data=music_data)
            if music_serializer.is_valid():
                music_serializer.save()
                return JsonResponse({'mess': 'Updated Successfully'}, safe=False)
            return JsonResponse("Failed to Update", safe=False, status=400)
        except Music.DoesNotExist:
            return JsonResponse({'mess': 'Record not found'}, status=404)
    
    elif request.method == 'DELETE':
        try:
            music = Music.objects.get(id_music=id_music)
            music.delete()
            return JsonResponse({'mess': 'Deleted Successfully'}, safe=False)
        except Music.DoesNotExist:
            return JsonResponse({'mess': 'Record not found'}, status=404)
        
@csrf_exempt
def musicApiHTML(request, id_music=0):
    if request.method == 'GET':
        if id_music == 0:
            music = Music.objects.all()
            music_serializer = MusicSerializer(music, many=True)
        else:
            try:
                music = Music.objects.get(id=id_music)  # Use 'id' instead of 'id_music'
                music_serializer = MusicSerializer(music)
            except Music.DoesNotExist:
                return JsonResponse({'mess': 'Record not found'}, status=404)
        
        # Pass the serialized music data to the template for rendering
        return render(request, 'index.html', {'musics': music_serializer.data})

@csrf_exempt
def userApi(request, id_user=0):
    if request.method == 'GET':
        if id_user == 0:
            user = User.objects.all()
            user_serializer = UserSerializer(user, many=True)
        else:
            try:
                user = User.objects.get(id_user=id_user)
                user_serializer = UserSerializer(user)
            except User.DoesNotExist:
                return JsonResponse({'mess': 'Record not found'}, status=404)
        return JsonResponse({'user':user_serializer.data}, safe=False)
        
    
    elif request.method == 'POST':
        user_data = JSONParser().parse(request)
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse({'mess': 'Added Successfully'}, safe=False)
        return JsonResponse("Failed to Add", safe=False, status=400)
    
    elif request.method == 'PUT':
        user_data = JSONParser().parse(request)
        try:
            user = User.objects.get(id_user=id_user)
            user_serializer = UserSerializer(user, data=user_data, partial=True)  # Use partial update
            if user_serializer.is_valid():
                user_serializer.save()
                return JsonResponse({'mess': 'Updated Successfully'}, safe=False)
            else:
                # Return detailed error messages
                return JsonResponse(user_serializer.errors, safe=False, status=400)
        except User.DoesNotExist:
            return JsonResponse({'mess': 'Record not found'}, status=404)
    
    elif request.method == 'DELETE':
        try:
            user = User.objects.get(id_user=id_user)
            user.delete()
            return JsonResponse({'mess': 'Deleted Successfully'}, safe=False)
        except User.DoesNotExist:
            return JsonResponse({'mess': 'Record not found'}, status=404)



@csrf_exempt
def singerApi(request, id_singer=0):
    if request.method == 'GET':
        if id_singer == 0:
            singer = Singer.objects.all()
            singer_serializer = SingerSerializer(singer, many=True)
        else:
            try:
                singer = Singer.objects.get(id_singer=id_singer)
                singer_serializer = SingerSerializer(singer)
            except Singer.DoesNotExist:
                return JsonResponse({'mess': 'Record not found'}, status=404)
        return JsonResponse({'singer':singer_serializer.data}, safe=False)
        
    
    elif request.method == 'POST':
        singer_data = JSONParser().parse(request)
        singer_serializer = SingerSerializer(data=singer_data)
        if singer_serializer.is_valid():
            singer_serializer.save()
            return JsonResponse({'mess': 'Added Successfully'}, safe=False)
        return JsonResponse("Failed to Add", safe=False, status=400)
    
    elif request.method == 'PUT':
        singer_data = JSONParser().parse(request)
        try:
            singer = Singer.objects.get(id_singer=id_singer)
            singer_serializer = SingerSerializer(singer, data=singer_data, partial=True)  # Use partial update
            if singer_serializer.is_valid():
                singer_serializer.save()
                return JsonResponse({'mess': 'Updated Successfully'}, safe=False)
            else:
                # Return detailed error messages
                return JsonResponse(singer_serializer.errors, safe=False, status=400)
        except Singer.DoesNotExist:
            return JsonResponse({'mess': 'Record not found'}, status=404)
    
    elif request.method == 'DELETE':
        try:
            singer = Singer.objects.get(id_singer=id_singer)
            singer.delete()
            return JsonResponse({'mess': 'Deleted Successfully'}, safe=False)
        except Singer.DoesNotExist:
            return JsonResponse({'mess': 'Record not found'}, status=404)


@csrf_exempt
def voteApi(request, id_vote=0):
    if request.method == 'GET':
        if id_vote == 0:
            vote = Vote.objects.all()
            vote_serializer = VoteSerializer(vote, many=True)
        else:
            try:
                vote = Vote.objects.get(id_vote=id_vote)
                vote_serializer = VoteSerializer(vote)
            except Vote.DoesNotExist:
                return JsonResponse({'mess': 'Record not found'}, status=404)
        return JsonResponse({'vote':vote_serializer.data}, safe=False)
        
    
    elif request.method == 'POST':
        vote_data = JSONParser().parse(request)
        vote_serializer = VoteSerializer(data=vote_data)
        if vote_serializer.is_valid():
            vote_serializer.save()
            return JsonResponse({'mess': 'Added Successfully'}, safe=False)
        return JsonResponse("Failed to Add", safe=False, status=400)
    
    elif request.method == 'PUT':
        vote_data = JSONParser().parse(request)
        try:
            vote = Vote.objects.get(id_vote=id_vote)
            vote_serializer = VoteSerializer(vote, data=vote_data, partial=True)  # Use partial update
            if vote_serializer.is_valid():
                vote_serializer.save()
                return JsonResponse({'mess': 'Updated Successfully'}, safe=False)
            else:
                # Return detailed error messages
                return JsonResponse(vote_serializer.errors, safe=False, status=400)
        except Vote.DoesNotExist:
            return JsonResponse({'mess': 'Record not found'}, status=404)
    
    elif request.method == 'DELETE':
        try:
            vote = Vote.objects.get(id_vote=id_vote)
            vote.delete()
            return JsonResponse({'mess': 'Deleted Successfully'}, safe=False)
        except Vote.DoesNotExist:
            return JsonResponse({'mess': 'Record not found'}, status=404)
            

@csrf_exempt
def transactionApi(request, id_transaction=0):
    try:
        if request.method == 'GET':
            if id_transaction == 0:
                transaction = Transaction.objects.all()
                transaction_serializer = TransactionSerializer(transaction, many=True)
            else:
                transaction = Transaction.objects.get(id_transaction=id_transaction)
                transaction_serializer = TransactionSerializer(transaction)
            return JsonResponse(transaction_serializer.data, safe= False)
        
        elif request.method == 'POST':
            transaction_data = JSONParser().parse(request)
            transaction_serializer = TransactionSerializer(data=transaction_data)
            if transaction_serializer.is_valid():
                transaction_serializer.save()
                return JsonResponse({'mess': 'Added Successfully'}, safe= False)
            return JsonResponse(transaction_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'PUT':
            transaction_data = JSONParser().parse(request)
            transaction = Transaction.objects.get(id_transaction=id_transaction)
            transaction_serializer = TransactionSerializer(transaction, data=transaction_data)
            if transaction_serializer.is_valid():
                transaction_serializer.save()
                return JsonResponse({'mess': 'Updated Successfully'}, safe= False)
            return JsonResponse(transaction_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            transaction = Transaction.objects.get(id_transaction=id_transaction)
            transaction.delete()
            return JsonResponse({'mess': 'Deleted Successfully'}, safe= False)
    except Transaction.DoesNotExist:
        return JsonResponse({'mess': 'Record not found'}, status=status.HTTP_404_NOT_FOUND)




@csrf_exempt
def albumApi(request, id_album=0):
    if request.method == 'GET':
        if id_album == 0:
            album = Album.objects.all()
            album_serializer = AlbumSerializer(album, many=True)
        else:
            try:
                album = Album.objects.get(id_album=id_album)
                album_serializer = AlbumSerializer(album)
            except Album.DoesNotExist:
                return JsonResponse({'mess': 'Record not found'}, status=404)
        return JsonResponse({'album':album_serializer.data}, safe=False)
        
    
    elif request.method == 'POST':
        album_data = JSONParser().parse(request)
        album_serializer = AlbumSerializer(data=album_data)
        if album_serializer.is_valid():
            album_serializer.save()
            return JsonResponse({'mess': 'Added Successfully'}, safe=False)
        return JsonResponse("Failed to Add", safe=False, status=400)
    
    elif request.method == 'PUT':
        album_data = JSONParser().parse(request)
        try:
            album = Album.objects.get(id_album=id_album)
            album_serializer = AlbumSerializer(album, data=album_data, partial=True)  # Use partial update
            if album_serializer.is_valid():
                album_serializer.save()
                return JsonResponse({'mess': 'Updated Successfully'}, safe=False)
            else:
                # Return detailed error messages
                return JsonResponse(album_serializer.errors, safe=False, status=400)
        except Album.DoesNotExist:
            return JsonResponse({'mess': 'Record not found'}, status=404)
    
    elif request.method == 'DELETE':
        try:
            album = Album.objects.get(id_album=id_album)
            album.delete()
            return JsonResponse({'mess': 'Deleted Successfully'}, safe=False)
        except Album.DoesNotExist:
            return JsonResponse({'mess': 'Record not found'}, status=404)
