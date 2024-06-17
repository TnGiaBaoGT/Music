from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from MusicApp.models import Music, User, Singer, Vote, Transaction, Album,Purchase, Like, MusicBundle,BundlePurchase
from MusicApp.serializers import MusicSerializer, UserSerializer, SingerSerializer, VoteSerializer, TransactionSerializer, AlbumSerializer,PurchaseSerializer, LikeSerializer,MusicBundleSerializer,BundlePurchaseSerializer
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.request import Request
import json
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

@csrf_exempt
def musicApi(request, id_music=0):
    # Wrap the WSGIRequest with DRF Request to use parsers
    drf_request = Request(request, parsers=[MultiPartParser(), FormParser()])

    if request.method == 'GET':
        if id_music == 0:
            # Retrieve all music items and order them by id_music
            music = Music.objects.all().order_by('id_music')
            music_serializer = MusicSerializer(music, many=True)
        else:
            try:
                music = Music.objects.get(id_music=id_music)
                music_serializer = MusicSerializer(music)
            except Music.DoesNotExist:
                return JsonResponse({'mess': 'Record not found'}, status=404)
        return JsonResponse({'music': music_serializer.data}, safe=False)

    elif request.method == 'POST':
        music_serializer = MusicSerializer(data=drf_request.data)
        if music_serializer.is_valid():
            music_serializer.save()
            return JsonResponse({'mess': 'Added Successfully'}, safe=False)
        else:
            # Print the errors to debug
            print(music_serializer.errors)
            return JsonResponse({'mess': 'Failed to Add', 'errors': music_serializer.errors}, safe=False, status=400)

    elif request.method == 'PUT':
        try:
            music = Music.objects.get(id_music=id_music)
            music_serializer = MusicSerializer(music, data=drf_request.data)
            if music_serializer.is_valid():
                music_serializer.save()
                return JsonResponse({'mess': 'Updated Successfully'}, safe=False)
            return JsonResponse({'mess': 'Failed to Update'}, safe=False, status=400)
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
