from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from MusicApp.models import Music, User, Singer, Vote, Transaction, Album,Purchase, Like, MusicBundle,BundlePurchase,Listen,MusicCart,MusicPurchased,MusicPurchasedItem,ComposerEarnings,ComposerEarningsDetail
from MusicApp.serializers import MusicSerializer, UserSerializer, SingerSerializer, VoteSerializer, TransactionSerializer, AlbumSerializer,PurchaseSerializer, LikeSerializer,MusicBundleSerializer,BundlePurchaseSerializer,MusicCartSerializer,MusicPurchasedSerializer,ComposerEarningsSerializer,ComposerEarningsDetailSerializer
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.request import Request
import json
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from datetime import datetime
from django.db.models import F


@csrf_exempt
def musicApi(request, id_user=0, id_music=0):
    # Wrap the WSGIRequest with DRF Request to use parsers
    drf_request = Request(request, parsers=[MultiPartParser(), FormParser()])

    if request.method == 'GET':
        if id_music == 0:
            if id_user == 0:
                # Retrieve all music items and order them by id_music
                music = Music.objects.all().order_by('id_music')
            else:
                # Retrieve all music items for the given composer and order them by id_music
                music = Music.objects.filter(composer=id_user).order_by('id_music')
            music_serializer = MusicSerializer(music, many=True)
        else:
            try:
                music = Music.objects.get(id_music=id_music, composer=id_user)
                music_serializer = MusicSerializer(music)
            except Music.DoesNotExist:
                return JsonResponse({'mess': 'Record not found'}, status=404)
        return JsonResponse({'music': music_serializer.data}, safe=False)

    elif request.method == 'POST':
        music_serializer = MusicSerializer(data=drf_request.data)
        if music_serializer.is_valid():
            music = music_serializer.save()

            # Create ComposerEarnings record for the current month
            composer = music.composer
            current_month = music.upload_date
            ComposerEarnings.objects.get_or_create(
                composer=composer,
                month=current_month,
                music = music,
                defaults={'earnings': 0, 'purchase_count': 0,'view_count': 0}
            )

            return JsonResponse({'mess': 'Added Successfully'}, safe=False)
        return JsonResponse({'mess': 'Failed to Add'}, safe=False, status=400)
    
    elif request.method == 'PUT':
        try:
            music = Music.objects.get(id_music=id_music)
            music_serializer = MusicSerializer(music, data=drf_request.data, partial=True)  # Use partial update
            if music_serializer.is_valid():
                music_serializer.save()
                return JsonResponse({'mess': 'Updated Successfully'}, safe=False)
            return JsonResponse(music_serializer.errors, safe=False, status=400)
        except Music.DoesNotExist:
            return JsonResponse({'mess': 'Record not found'}, status=404)
    
    elif request.method == 'DELETE':
        try:
            music = Music.objects.get(id_music=id_music)
            music.delete()
            return JsonResponse({'mess': 'Deleted Successfully'}, safe=False)
        except Music.DoesNotExist:
            return JsonResponse({'mess': 'Record not found'}, status=404)
    
    return HttpResponseNotAllowed(['GET', 'POST', 'PUT', 'DELETE'])
        
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
def like_music(request, music_id):
    if request.method == 'POST':
        music = get_object_or_404(Music, id_music=music_id)
        
        # Get the JSON data from the request body
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        
        if user_id:
            user_exists = User.objects.filter(id_user=user_id).exists()
            if user_exists:
                like, created = Like.objects.get_or_create(user_id=user_id, music=music)
                if created:
                    music.num_vote += 1
                    music.save()
                    return JsonResponse({'status': 'liked', 'music_id': music_id})
                else:
                    return JsonResponse({'status': 'already liked', 'music_id': music_id})
            else:
                return JsonResponse({'error': 'User does not exist'}, status=404)
        else:
            return JsonResponse({'error': 'user_id is missing'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)



@csrf_exempt
def unlike_music(request, music_id):
    if request.method == 'POST':
        music = get_object_or_404(Music, id_music=music_id)
        
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        
        if user_id:
            user_exists = User.objects.filter(id_user=user_id).exists()
            if user_exists:
                like = Like.objects.filter(user_id=user_id, music=music)
                if like.exists():
                    like.delete()
                    music.num_vote = max(0, music.num_vote - 1)
                    music.save()
                    return JsonResponse({'status': 'unliked', 'music_id': music_id})
                else:
                    return JsonResponse({'status': 'not liked', 'music_id': music_id})
            else:
                return JsonResponse({'error': 'User does not exist'}, status=404)
        else:
            return JsonResponse({'error': 'user_id is missing'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)
    

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
    if request.method == 'GET':
        if id_transaction == 0:
            transaction = Transaction.objects.all()
            transaction_serializer = TransactionSerializer(transaction, many=True)
        else:
            try:
                transaction = Transaction.objects.get(id_transaction=id_transaction)
                transaction_serializer = TransactionSerializer(transaction)
            except Transaction.DoesNotExist:
                return JsonResponse({'mess': 'Record not found'}, status=404)
        return JsonResponse({'transaction':transaction_serializer.data}, safe=False)
        
    
    elif request.method == 'POST':
        transaction_data = JSONParser().parse(request)
        transaction_serializer = TransactionSerializer(data=transaction_data)
        if transaction_serializer.is_valid():
            transaction_serializer.save()
            return JsonResponse({'mess': 'Added Successfully'}, safe=False)
        return JsonResponse("Failed to Add", safe=False, status=400)
    
    elif request.method == 'PUT':
        transaction_data = JSONParser().parse(request)
        try:
            transaction = Transaction.objects.get(id_transaction=id_transaction)
            transaction_serializer = TransactionSerializer(transaction, data=transaction_data, partial=True)  # Use partial update
            if transaction_serializer.is_valid():
                transaction_serializer.save()
                return JsonResponse({'mess': 'Updated Successfully'}, safe=False)
            else:
                # Return detailed error messages
                return JsonResponse(transaction_serializer.errors, safe=False, status=400)
        except Transaction.DoesNotExist:
            return JsonResponse({'mess': 'Record not found'}, status=404)
    
    elif request.method == 'DELETE':
        try:
            transaction = Transaction.objects.get(id_transaction=id_transaction)
            transaction.delete()
            return JsonResponse({'mess': 'Deleted Successfully'}, safe=False)
        except Transaction.DoesNotExist:
            return JsonResponse({'mess': 'Record not found'}, status=404)



@csrf_exempt
def albumApi(request, id_album=0, id_user=0):
    if request.method == 'GET':
        if id_user > 0:
            try:
                album = Album.objects.filter(user_id_album=id_user).order_by('id_album')
                album_serializer = AlbumSerializer(album, many=True)
                return JsonResponse({'album': album_serializer.data}, safe=False)
            except ObjectDoesNotExist:
                return JsonResponse({'mess': 'Record not found'}, status=404)
        
        if id_album > 0:
            try:
                album = Album.objects.get(id_album=id_album)
                album_serializer = AlbumSerializer(album)
                return JsonResponse({'album': album_serializer.data}, safe=False)
            except Album.DoesNotExist:
                return JsonResponse({'mess': 'Record not found'}, status=404)
        
        album = Album.objects.all().order_by('id_album')
        album_serializer = AlbumSerializer(album, many=True)
        return JsonResponse({'album': album_serializer.data}, safe=False)
    
    elif request.method == 'POST':
        album_data = JSONParser().parse(request)
        album_serializer = AlbumSerializer(data=album_data)
        if album_serializer.is_valid():
            album_serializer.save()
            return JsonResponse({'mess': 'Added Successfully'}, safe=False)
        return JsonResponse(album_serializer.errors, safe=False, status=400)
    
    elif request.method == 'PUT':
        album_data = JSONParser().parse(request)
        try:
            album = Album.objects.get(id_album=id_album)
            album_serializer = AlbumSerializer(album, data=album_data, partial=True)  # Use partial update
            if album_serializer.is_valid():
                album_serializer.save()
                return JsonResponse({'mess': 'Updated Successfully'}, safe=False)
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


@csrf_exempt
def purchaseApi(request, id_purchase=0, id_user=0):
    if request.method == 'GET':
        if id_user > 0:
            try:
                purchase = Purchase.objects.filter(user_id=id_user).order_by('id_purchase')
                purchase_serializer = PurchaseSerializer(purchase, many=True)
                return JsonResponse({'purchase': purchase_serializer.data}, safe=False)
            except ObjectDoesNotExist:
                return JsonResponse({'mess': 'Record not found'}, status=404)
        
        if id_purchase > 0:
            try:
                purchase = Purchase.objects.get(id_purchase=id_purchase)
                purchase_serializer = PurchaseSerializer(purchase)
                return JsonResponse({'purchase': purchase_serializer.data}, safe=False)
            except Purchase.DoesNotExist:
                return JsonResponse({'mess': 'Record not found'}, status=404)
        
        purchase = Purchase.objects.all().order_by('id_purchase')
        purchase_serializer = PurchaseSerializer(purchase, many=True)
        return JsonResponse({'purchase': purchase_serializer.data}, safe=False)
    
    elif request.method == 'POST':
        purchase_data = JSONParser().parse(request)
        user_id = purchase_data.get('user')
        bundle_id = purchase_data.get('bundle')
        
        # Check for duplicate
        if user_id and bundle_id:
            duplicate_purchase = Purchase.objects.filter(user_id=user_id, bundle_id=bundle_id).exists()
            if duplicate_purchase:
                return JsonResponse({'mess': 'Duplicate purchase not allowed'}, safe=False, status=400)
        
        purchase_serializer = PurchaseSerializer(data=purchase_data)
        if purchase_serializer.is_valid():
            purchase_serializer.save()
            return JsonResponse({'mess': 'Added Successfully'}, safe=False)
        return JsonResponse(purchase_serializer.errors, safe=False, status=400)
    
    elif request.method == 'PUT':
        purchase_data = JSONParser().parse(request)
        try:
            purchase = Purchase.objects.get(id_purchase=id_purchase)
            purchase_serializer = PurchaseSerializer(purchase, data=purchase_data, partial=True)  # Use partial update
            if purchase_serializer.is_valid():
                purchase_serializer.save()
                return JsonResponse({'mess': 'Updated Successfully'}, safe=False)
            return JsonResponse(purchase_serializer.errors, safe=False, status=400)
        except Purchase.DoesNotExist:
            return JsonResponse({'mess': 'Record not found'}, status=404)
    
    elif request.method == 'DELETE':
        try:
            purchase = Purchase.objects.get(id_purchase=id_purchase)
            purchase.delete()
            return JsonResponse({'mess': 'Deleted Successfully'}, safe=False)
        except Purchase.DoesNotExist:
            return JsonResponse({'mess': 'Record not found'}, status=404)


@csrf_exempt
def likeApi(request, id_like=0, id_user=0):
    if request.method == 'GET':
        if id_user > 0:
            try:
                like = Like.objects.filter(user=id_user).order_by('timestamp')
                like_serializer = LikeSerializer(like, many=True)
                return JsonResponse({'like': like_serializer.data}, safe=False)
            except ObjectDoesNotExist:
                return JsonResponse({'mess': 'Record not found'}, status=404)
        
        if id_like > 0:
            try:
                like = Like.objects.get(id_like=id_like)
                like_serializer = LikeSerializer(like)
                return JsonResponse({'like': like_serializer.data}, safe=False)
            except Like.DoesNotExist:
                return JsonResponse({'mess': 'Record not found'}, status=404)
        
        like = Like.objects.all().order_by('timestamp')
        like_serializer = LikeSerializer(like, many=True)
        return JsonResponse({'like': like_serializer.data}, safe=False)
    
    elif request.method == 'POST':
        like_data = JSONParser().parse(request)
        like_serializer = LikeSerializer(data=like_data)
        if like_serializer.is_valid():
            like_serializer.save()
            return JsonResponse({'mess': 'Added Successfully'}, safe=False)
        return JsonResponse(like_serializer.errors, safe=False, status=400)
    
    elif request.method == 'PUT':
        like_data = JSONParser().parse(request)
        try:
            like = Like.objects.get(id_like=id_like)
            like_serializer = LikeSerializer(like, data=like_data, partial=True)  # Use partial update
            if like_serializer.is_valid():
                like_serializer.save()
                return JsonResponse({'mess': 'Updated Successfully'}, safe=False)
            return JsonResponse(like_serializer.errors, safe=False, status=400)
        except Like.DoesNotExist:
            return JsonResponse({'mess': 'Record not found'}, status=404)
    
    elif request.method == 'DELETE':
        try:
            like = Like.objects.get(id_like=id_like)
            like.delete()
            return JsonResponse({'mess': 'Deleted Successfully'}, safe=False)
        except Like.DoesNotExist:
            return JsonResponse({'mess': 'Record not found'}, status=404)


@csrf_exempt
def musicbundleApi(request, id_musicbundle=0):
    if request.method == 'GET':
        if id_musicbundle == 0:
            musicbundle = MusicBundle.objects.all().order_by('id_bundle')
            musicbundle_serializer = MusicBundleSerializer(musicbundle, many=True)
        else:
            try:
                musicbundle = MusicBundle.objects.get(id_musicbundle=id_musicbundle)
                musicbundle_serializer = MusicBundleSerializer(musicbundle)
            except MusicBundle.DoesNotExist:
                return JsonResponse({'mess': 'Record not found'}, status=404)
        return JsonResponse({'musicbundle':musicbundle_serializer.data}, safe=False)
        
    
    elif request.method == 'POST':
        musicbundle_data = JSONParser().parse(request)
        musicbundle_serializer = MusicBundleSerializer(data=musicbundle_data)
        if musicbundle_serializer.is_valid():
            musicbundle_serializer.save()
            return JsonResponse({'mess': 'Added Successfully'}, safe=False)
        return JsonResponse("Failed to Add", safe=False, status=400)
    
    elif request.method == 'PUT':
        musicbundle_data = JSONParser().parse(request)
        try:
            musicbundle = MusicBundle.objects.get(id_musicbundle=id_musicbundle)
            musicbundle_serializer = MusicBundleSerializer(musicbundle, data=musicbundle_data, partial=True)  # Use partial update
            if musicbundle_serializer.is_valid():
                musicbundle_serializer.save()
                return JsonResponse({'mess': 'Updated Successfully'}, safe=False)
            else:
                # Return detailed error messages
                return JsonResponse(musicbundle_serializer.errors, safe=False, status=400)
        except MusicBundle.DoesNotExist:
            return JsonResponse({'mess': 'Record not found'}, status=404)
    
    elif request.method == 'DELETE':
        try:
            musicbundle = MusicBundle.objects.get(id_musicbundle=id_musicbundle)
            musicbundle.delete()
            return JsonResponse({'mess': 'Deleted Successfully'}, safe=False)
        except MusicBundle.DoesNotExist:
            return JsonResponse({'mess': 'Record not found'}, status=404)
        

@csrf_exempt
def bundlepurchaseApi(request, id_bundlepurchase=0, id_user=0):
    if request.method == 'GET':
        if id_user > 0:
            try:
                bundlepurchase = BundlePurchase.objects.filter(user_id=id_user).order_by('id_bundle_purchase')
                bundlepurchase_serializer = BundlePurchaseSerializer(bundlepurchase, many=True)
                return JsonResponse({'bundlepurchase': bundlepurchase_serializer.data}, safe=False)
            except ObjectDoesNotExist:
                return JsonResponse({'mess': 'Record not found'}, status=404)
        
        if id_bundlepurchase > 0:
            try:
                bundlepurchase = BundlePurchase.objects.get(id_bundle_purchase=id_bundlepurchase)
                bundlepurchase_serializer = BundlePurchaseSerializer(bundlepurchase)
                return JsonResponse({'bundlepurchase': bundlepurchase_serializer.data}, safe=False)
            except BundlePurchase.DoesNotExist:
                return JsonResponse({'mess': 'Record not found'}, status=404)
        
        bundlepurchase = BundlePurchase.objects.all().order_by('id_bundle_purchase')
        bundlepurchase_serializer = BundlePurchaseSerializer(bundlepurchase, many=True)
        return JsonResponse({'bundlepurchase': bundlepurchase_serializer.data}, safe=False)
    
    elif request.method == 'POST':
        bundlepurchase_data = JSONParser().parse(request)
        bundlepurchase_serializer = BundlePurchaseSerializer(data=bundlepurchase_data)
        if bundlepurchase_serializer.is_valid():
            bundlepurchase_serializer.save()
            return JsonResponse({'mess': 'Added Successfully'}, safe=False)
        return JsonResponse(bundlepurchase_serializer.errors, safe=False, status=400)
    
    elif request.method == 'PUT':
        bundlepurchase_data = JSONParser().parse(request)
        try:
            bundlepurchase = BundlePurchase.objects.get(id_bundle_purchase=id_bundlepurchase)
            bundlepurchase_serializer = BundlePurchaseSerializer(bundlepurchase, data=bundlepurchase_data, partial=True)  # Use partial update
            if bundlepurchase_serializer.is_valid():
                bundlepurchase_serializer.save()
                return JsonResponse({'mess': 'Updated Successfully'}, safe=False)
            return JsonResponse(bundlepurchase_serializer.errors, safe=False, status=400)
        except BundlePurchase.DoesNotExist:
            return JsonResponse({'mess': 'Record not found'}, status=404)
    
    elif request.method == 'DELETE':
        try:
            bundlepurchase = BundlePurchase.objects.get(id_bundle_purchase=id_bundlepurchase)
            bundlepurchase.delete()
            return JsonResponse({'mess': 'Deleted Successfully'}, safe=False)
        except BundlePurchase.DoesNotExist:
            return JsonResponse({'mess': 'Record not found'}, status=404)

@csrf_exempt
def confirm_purchase(request, id_purchase):
    if request.method == 'POST':
        try:
            # Retrieve the pending purchase object
            pending_purchase = get_object_or_404(Purchase, pk=id_purchase)

            # Check if the purchase has a momo_token
            if not pending_purchase.momo_token:
                return JsonResponse({'error': 'MoMo token not found for this purchase'}, status=400)

            # Create the BundlePurchase instance
            bundle_purchase = BundlePurchase.objects.create(
                user=pending_purchase.user,
                bundle=pending_purchase.bundle,
                momo_token=pending_purchase.momo_token,
                purchase_date=timezone.now()
            )

            # Delete the pending purchase instance
            pending_purchase.delete()

            # Serialize the bundle purchase object
            serializer = BundlePurchaseSerializer(bundle_purchase)

            # Return a success response with the serialized data
            return JsonResponse(serializer.data, status=201)
        except Exception as e:
            # Return an error response if something goes wrong
            return JsonResponse({'error': str(e)}, status=500)
    else:
        # Handle other HTTP methods (GET, PUT, DELETE) if necessary
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)

@csrf_exempt
def receive_momo_token(request):
    if request.method == 'POST':
        id_purchase = request.POST.get('id_purchase')
        momo_token = request.POST.get('momo_token')

        if not id_purchase or not momo_token:
            return JsonResponse({'error': 'Missing purchase ID or token'}, status=400)

        purchase = get_object_or_404(Purchase, pk=id_purchase)
        purchase.momo_token = momo_token
        purchase.save()

        return JsonResponse({'success': 'Token saved successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)


@csrf_exempt
def listen_song(request, id_music):
    if request.method == 'POST':
        try:
            # Retrieve the music object
            song = get_object_or_404(Music, id_music=id_music)
            
            # Retrieve or create ComposerEarnings record for the upload month of the music
            composer = song.composer
            upload_month = song.upload_date  # Set to the first day of the month
            earnings_record, created = ComposerEarnings.objects.get_or_create(
                composer=composer,
                music=song,
                month=upload_month,
                defaults={'earnings': 0, 'purchase_count': 0, 'view_count': 0}
            )

            # Assuming user_id is sent in the request body
            data = json.loads(request.body)
            user_id = data.get('user_id')
            user = None

            if user_id:
                user = get_object_or_404(User, id_user=user_id)

            # Record the listen
            Listen.objects.create(music=song, user=user)

            # Increment the listen count for the music
            song.listen_count += 1
            song.save()

            # Update the view count for ComposerEarnings
            earnings_record.view_count += 1
            earnings_record.save()

            return JsonResponse({"message": "Song listened"}, status=200)
        
        except Music.DoesNotExist:
            return JsonResponse({"error": "Song not found"}, status=404)
        
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    else:
        return JsonResponse({"error": "Invalid HTTP method"}, status=405)


@csrf_exempt
def musiccartApi(request, id_cart=0, id_user=0):
    if request.method == 'GET':
        if id_user > 0:
            musiccart = MusicCart.objects.filter(user_id=id_user).order_by('id_cart')
            if musiccart.exists():
                musiccart_serializer = MusicCartSerializer(musiccart, many=True)
                return JsonResponse({'musiccart': musiccart_serializer.data}, safe=False)
            else:
                return JsonResponse({'mess': 'Record not found'}, status=404)
        
        if id_cart > 0:
            try:
                musiccart = MusicCart.objects.get(id_cart=id_cart)
                musiccart_serializer = MusicCartSerializer(musiccart)
                return JsonResponse({'musiccart': musiccart_serializer.data}, safe=False)
            except MusicCart.DoesNotExist:
                return JsonResponse({'mess': 'Record not found'}, status=404)
        
        musiccart = MusicCart.objects.all().order_by('id_cart')
        musiccart_serializer = MusicCartSerializer(musiccart, many=True)
        return JsonResponse({'musiccart': musiccart_serializer.data}, safe=False)
    
    elif request.method == 'POST':
        musiccart_data = JSONParser().parse(request)
        user_id = musiccart_data.get('user')
        music_id = musiccart_data.get('music')

        if not user_id or not music_id:
            return JsonResponse({'mess': 'User ID and Music ID are required'}, safe=False, status=400)

        # Check for duplicate active cart for the user
        if MusicCart.objects.filter(user_id=user_id, music_id=music_id).exists():
            return JsonResponse({'mess': 'Duplicate music entry not allowed in user\'s cart'}, safe=False, status=400)

        musiccart_serializer = MusicCartSerializer(data=musiccart_data)
        if musiccart_serializer.is_valid():
            musiccart_serializer.save()
            return JsonResponse({'mess': 'Added Successfully'}, safe=False)
        return JsonResponse(musiccart_serializer.errors, safe=False, status=400)
    
    elif request.method == 'PUT':
        musiccart_data = JSONParser().parse(request)
        try:
            musiccart = MusicCart.objects.get(id_cart=id_cart)
            musiccart_serializer = MusicCartSerializer(musiccart, data=musiccart_data, partial=True)  # Use partial update
            if musiccart_serializer.is_valid():
                musiccart_serializer.save()
                return JsonResponse({'mess': 'Updated Successfully'}, safe=False)
            return JsonResponse(musiccart_serializer.errors, safe=False, status=400)
        except MusicCart.DoesNotExist:
            return JsonResponse({'mess': 'Record not found'}, status=404)
    
    elif request.method == 'DELETE':
        try:
            musiccart = MusicCart.objects.get(id_cart=id_cart)
            musiccart.delete()
            return JsonResponse({'mess': 'Deleted Successfully'}, safe=False)
        except MusicCart.DoesNotExist:
            return JsonResponse({'mess': 'Record not found'}, status=404)

@csrf_exempt
def musicpurchasedApi(request, id_music_purchased=0, id_user=0):
    if request.method == 'GET':
        if id_user > 0:
            try:
                musicpurchased = MusicPurchased.objects.filter(user_id=id_user).order_by('id_music_purchased')
                musicpurchased_serializer = MusicPurchasedSerializer(musicpurchased, many=True)
                return JsonResponse({'musicpurchased': musicpurchased_serializer.data}, safe=False)
            except ObjectDoesNotExist:
                return JsonResponse({'mess': 'Record not found'}, status=404)
        
        if id_music_purchased > 0:
            try:
                musicpurchased = MusicPurchased.objects.get(id_music_purchased=id_music_purchased)
                musicpurchased_serializer = MusicPurchasedSerializer(musicpurchased)
                return JsonResponse({'musicpurchased': musicpurchased_serializer.data}, safe=False)
            except MusicPurchased.DoesNotExist:
                return JsonResponse({'mess': 'Record not found'}, status=404)
        
        musicpurchased = MusicPurchased.objects.all().order_by('id_music_purchased')
        musicpurchased_serializer = MusicPurchasedSerializer(musicpurchased, many=True)
        return JsonResponse({'musicpurchased': musicpurchased_serializer.data}, safe=False)
    
    elif request.method == 'POST':
        musicpurchased_data = JSONParser().parse(request)
        user_id = musicpurchased_data.get('user')
        
        # Check for duplicate active cart for the user
        if user_id:
            duplicate_musicpurchased = MusicPurchased.objects.filter(user_id=user_id, is_active=True).exists()
            if duplicate_musicpurchased:
                return JsonResponse({'mess': 'Duplicate active musicpurchased not allowed'}, safe=False, status=400)
        
        musicpurchased_serializer = MusicPurchasedSerializer(data=musicpurchased_data)
        if musicpurchased_serializer.is_valid():
            musicpurchased_serializer.save()
            return JsonResponse({'mess': 'Added Successfully'}, safe=False)
        return JsonResponse(musicpurchased_serializer.errors, safe=False, status=400)
    
    elif request.method == 'PUT':
        musicpurchased_data = JSONParser().parse(request)
        try:
            musicpurchased = MusicPurchased.objects.get(id_music_purchased=id_music_purchased)
            musicpurchased_serializer = MusicPurchasedSerializer(musicpurchased, data=musicpurchased_data, partial=True)  # Use partial update
            if musicpurchased_serializer.is_valid():
                musicpurchased_serializer.save()
                return JsonResponse({'mess': 'Updated Successfully'}, safe=False)
            return JsonResponse(musicpurchased_serializer.errors, safe=False, status=400)
        except MusicPurchased.DoesNotExist:
            return JsonResponse({'mess': 'Record not found'}, status=404)
    
    elif request.method == 'DELETE':
        try:
            musicpurchased = MusicPurchased.objects.get(id_music_purchased=id_music_purchased)
            musicpurchased.delete()
            return JsonResponse({'mess': 'Deleted Successfully'}, safe=False)
        except MusicPurchased.DoesNotExist:
            return JsonResponse({'mess': 'Record not found'}, status=404)


@csrf_exempt
def confirm_music_purchase(request, id_user):
    if request.method == 'POST':
        try:
            # Retrieve the user instance
            user = User.objects.get(pk=id_user)
            
            # Retrieve all cart items for the user
            cart_items = MusicCart.objects.filter(user=user)

            if not cart_items.exists():
                return JsonResponse({'error': 'No items in the cart'}, status=400)

            # Check if all cart items have the same momo_token
            momo_tokens = {item.momo_token for item in cart_items}
            if len(momo_tokens) != 1 or None in momo_tokens:
                return JsonResponse({'error': 'All cart items must have a valid momo_token'}, status=400)

            momo_token = momo_tokens.pop()  # Get the unique momo_token

            # Create the MusicPurchased instance
            music_purchased = MusicPurchased.objects.create(
                user=user,
                momo_token=momo_token,
                purchase_date=timezone.now()
            )

            # Add each music item from the cart to the purchased music
            for item in cart_items:
                MusicPurchasedItem.objects.create(
                    music_purchased=music_purchased,
                    music=item.music
                )

                # Update composer earnings
                composer = item.music.composer
                earning_amount = item.music.price_music * 0.7
                upload_month = item.music.upload_date  # Set day to 1

                # Ensure ComposerEarnings record exists for upload month
                earnings_record, created = ComposerEarnings.objects.get_or_create(
                    composer=composer,
                    music=item.music,
                    month=upload_month,
                    defaults={'earnings': 0, 'purchase_count': 0, 'view_count': 0}
                )

                # Update earnings and purchase count
                earnings_record.earnings = F('earnings') + earning_amount
                earnings_record.purchase_count = F('purchase_count') + 1
                earnings_record.save()

            # Delete all cart items for the user
            cart_items.delete()

            # Serialize the music purchase object
            serializer = MusicPurchasedSerializer(music_purchased)

            # Return a success response with the serialized data
            return JsonResponse(serializer.data, status=201)
        
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        
        except Exception as e:
            # Return an error response if something goes wrong
            return JsonResponse({'error': str(e)}, status=500)
    
    else:
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)


@csrf_exempt
def receive_momo_token_music(request):
    if request.method == 'POST':
        id_user = request.POST.get('id_user')  # Assuming you pass the user ID in the POST request
        momo_token = request.POST.get('momo_token')

        if not id_user or not momo_token:
            return JsonResponse({'error': 'Missing user ID or token'}, status=400)

        # Retrieve all cart items for the user
        cart_items = MusicCart.objects.filter(user=id_user)

        if not cart_items.exists():
            return JsonResponse({'error': 'No items in the cart for the user'}, status=400)

        # Update the momo_token for each cart item
        for item in cart_items:
            item.momo_token = momo_token
            item.save()

        return JsonResponse({'success': 'Token saved successfully to all cart items'}, status=200)
    else:
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)

@csrf_exempt
def composer_earnings_api(request, id_composer_earnings=0, id_composer=0):
    if request.method == 'GET':
        if id_composer > 0:
            try:
                earnings = ComposerEarnings.objects.filter(composer=id_composer).order_by('month')
                earnings_serializer = ComposerEarningsSerializer(earnings, many=True)
                return JsonResponse({'composer_earnings': earnings_serializer.data}, safe=False)
            except ComposerEarnings.DoesNotExist:
                return JsonResponse({'mess': 'Record not found'}, status=404)
        
        if id_composer_earnings > 0:
            try:
                earnings = ComposerEarnings.objects.get(id=id_composer_earnings)
                earnings_serializer = ComposerEarningsSerializer(earnings)
                return JsonResponse({'composer_earnings': earnings_serializer.data}, safe=False)
            except ComposerEarnings.DoesNotExist:
                return JsonResponse({'mess': 'Record not found'}, status=404)
        
        earnings = ComposerEarnings.objects.all().order_by('month')
        earnings_serializer = ComposerEarningsSerializer(earnings, many=True)
        return JsonResponse({'composer_earnings': earnings_serializer.data}, safe=False)
    
    elif request.method == 'POST':
        earnings_data = JSONParser().parse(request)
        earnings_serializer = ComposerEarningsSerializer(data=earnings_data)
        if earnings_serializer.is_valid():
            earnings_serializer.save()
            return JsonResponse({'mess': 'Added Successfully'}, safe=False)
        return JsonResponse(earnings_serializer.errors, safe=False, status=400)
    
    elif request.method == 'PUT':
        earnings_data = JSONParser().parse(request)
        try:
            earnings = ComposerEarnings.objects.get(id=id_composer_earnings)
            earnings_serializer = ComposerEarningsSerializer(earnings, data=earnings_data, partial=True)  # Use partial update
            if earnings_serializer.is_valid():
                earnings_serializer.save()
                return JsonResponse({'mess': 'Updated Successfully'}, safe=False)
            return JsonResponse(earnings_serializer.errors, safe=False, status=400)
        except ComposerEarnings.DoesNotExist:
            return JsonResponse({'mess': 'Record not found'}, status=404)
    
    elif request.method == 'DELETE':
        try:
            earnings = ComposerEarnings.objects.get(id=id_composer_earnings)
            earnings.delete()
            return JsonResponse({'mess': 'Deleted Successfully'}, safe=False)
        except ComposerEarnings.DoesNotExist:
            return JsonResponse({'mess': 'Record not found'}, status=404)


@csrf_exempt
def composer_earnings_detail(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            earnings_id = data.get('composer_earnings_id')

            composer_earnings = ComposerEarnings.objects.get(pk=earnings_id)

            # Get or create the detail record
            detail, created = ComposerEarningsDetail.objects.get_or_create(
                composer_earnings=composer_earnings
            )

            # Calculate total earnings
            detail.calculate_total_earnings()
            detail.save()

            return JsonResponse({
                'message': 'Composer earnings detail updated successfully' if not created else 'created successfully',
                'composer_earnings_detail': {
                    'id': detail.id,
                    'composer_earnings': detail.composer_earnings.id,
                    'momo_token': detail.momo_token,
                    'total_earnings': str(detail.total_earnings)
                }
            }, status=200 if not created else 201)

        except ComposerEarnings.DoesNotExist:
            return JsonResponse({'error': 'Composer earnings not found'}, status=404)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)


@csrf_exempt
def receive_momo_token_composer_earnings(request):
    if request.method == 'POST':
        composer_earnings_id = request.POST.get('composer_earnings_id')
        momo_token = request.POST.get('momo_token')

        if not composer_earnings_id or not momo_token:
            return JsonResponse({'error': 'Missing earnings ID or token'}, status=400)

        # Retrieve the ComposerEarningsDetail object
        detail = get_object_or_404(ComposerEarningsDetail, composer_earnings_id=composer_earnings_id)
        detail.momo_token = momo_token
        detail.save()

        return JsonResponse({'success': 'Token saved successfully'}, status=200)
    
    else:
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)


@csrf_exempt
def composer_earnings_detail_api(request, composer_earnings_id=0):
    if request.method == 'GET':
        if composer_earnings_id > 0:
            try:
                composer_earnings = ComposerEarnings.objects.get(pk=composer_earnings_id)
                composer_earnings_detail = ComposerEarningsDetail.objects.get(composer_earnings=composer_earnings)
                serializer = ComposerEarningsDetailSerializer(composer_earnings_detail)
                return JsonResponse(serializer.data, status=200)
            except ObjectDoesNotExist:
                return JsonResponse({'error': 'ComposerEarningsDetail not found for this ComposerEarnings'}, status=404)
        else:
            return JsonResponse({'error': 'Invalid composer_earnings_id'}, status=400)
