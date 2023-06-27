from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from backend.decorators import login_jwt_required, is_owner
from .models import Car, Comment, UnderComment
from .serializers import (
    CarSerializer, 
    CommentSerializer, 
    UnderCommentSerializer
)


# (important!) using params safe <JsonResponse(..., safe=<boolean>)> 
# in case where data is massive use true, in another case use false (default - true)
@csrf_exempt
@login_jwt_required
def car_list(request):
    try:
        cars = Car.objects.all()

    except cars.DoesNotExist:
        return HttpResponse(status=404)
    
    if request.method == 'GET':
        serializer = CarSerializer(cars, many=True)
        return JsonResponse(serializer.data)


# individual obj for spectate for all users
@csrf_exempt
@login_jwt_required
def car_obj_spectate(request, pk):
    try:
        car = Car.objects.get(pk=pk)
    
    except car.DoesNotExist:
        return HttpResponse(status=404)
    
    if request.method == 'GET':
        serializer = CarSerializer(car)
        return JsonResponse(serializer.data)


@csrf_exempt
@login_jwt_required
def car_create(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CarSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        # replace <serializer.errors> to 
        # smth else (like "bad input")
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@is_owner
def car_obj(request, pk, upk):
    try:
        car = Car.objects.get(pk=pk)
    
    except car.DoesNotExist:
        return HttpResponse(status=404)
    
    if request.mehthod == 'GET':
        serializer = CarSerializer(car)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = CarSerializer(car, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        # replace <serializer.errors> to 
        # smth else (like "bad input")
        return JsonResponse(serializer.errors, status=400)
        
    elif request.method == 'DELETE':
        car.delete()
        return JsonResponse("object was successfully deleted", status=204)


@csrf_exempt
@login_jwt_required
def comment_list(request, car_pk):
    try:
        comments = Comment.objects.filter(car_id=car_pk)

    except comments.DoesNotExist:
        return HttpResponse(status=404)
    
    if request.method == 'GET':
        serializer = CommentSerializer(comments)
        return JsonResponse(serializer.data)
    

@csrf_exempt
@login_jwt_required
def comment_create(request, car_pk):
    try:
        car = Car.objects.get(pk=car_pk)

    except car.DoesNotExist:
        return JsonResponse('car is not found', status=404, safe=False)
    
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
            # replace <serializer.errors> to 
            # smth else (like "bad input")
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@is_owner
def comment_obj(request, car_pk, pk):
    try:
        comment = Comment.objects.get(pk=pk, car_id=car_pk)

    except comment.DoesNotExist:
        return HttpResponse(status=404)
    
    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return JsonResponse(serializer.data)
    
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = CommentSerializer(comment, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        # replace <serializer.errors> to 
        # smth else (like "bad input")
        return JsonResponse(serializer.errors, status=400)
    
    elif request.method == 'DELETE':
        comment.delete()
        return JsonResponse("object was successfully deleted", status=204)


@csrf_exempt
@login_jwt_required
def undercomment_list(request, car_pk, comm_pk):
    try:
        undercomms = UnderComment.objects.filter(car_id=car_pk, comm_id=comm_pk)

    except undercomms.DoesNotExist:
        return HttpResponse(status=404)
    
    if request.method == 'GET':
        serializer = UnderCommentSerializer(undercomms)
        return JsonResponse(serializer.data)


@csrf_exempt
@login_jwt_required
def undercomment_create(request, car_pk, comm_pk):
    try:
        car = Car.objects.get(pk=car_pk)
        comment = Comment.objects.get(pk=comm_pk)

    except car.DoesNotExist:
        return JsonResponse('car is not found', status=404, safe=False)
    
    except comment.DoesNotExist:
        return JsonResponse('comment is not found', status=404, safe=False)
    
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UnderCommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        # replace <serializer.errors> to 
        # smth else (like "bad input")
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@is_owner
def undercomment_obj(request, car_pk, comm_pk, pk):
    try:
        undercomment = UnderComment.objects.filter(car_id=car_pk, comm_id=comm_pk, pk=pk)

    except undercomment.DoesNotExist:
        return HttpResponse(status=404)
    
    if request.method == 'GET':
        serializer = UnderCommentSerializer(undercomment)
        return JsonResponse(serializer.data)
    
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = UnderCommentSerializer(undercomment, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        # replace <serializer.errors> to 
        # smth else (like "bad input")
        return JsonResponse(serializer.errors, status=400)
    
    elif request.method == 'DELETE':
        undercomment.delete()
        return JsonResponse("object was successfully deleted", status=204)        
