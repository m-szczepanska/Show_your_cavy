from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from creatder.models import Creature, Review, User
from creatder.serializers import (GetCreatureSerializer,
    CreateCreatureSerializer, GetUserSerializer, CreateUserSerializer,
    UpdateUserSerializer, GetOwnCreatures, RateCreatureSerializer,
    # GetCreatureRatingSerializer)
    )


@csrf_exempt
def creature_list(request):
    """
    List all creatures.
    """
    if request.method == 'GET':
        creatures = Creature.objects.all()
        serializer = GetCreatureSerializer(creatures, many=True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def user_list(request):
    """
    List all users.
    """
    if request.method == 'GET':
        users = User.objects.all()
        serializer = GetUserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CreateUserSerializer(data=data)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        new_user = User(
            name=data['name'],
            login=data['login'],
            email=data['email']
        )
        new_user.set_password(data['password'])  # also saves the instance

        serializer_return = GetUserSerializer(new_user)
        return JsonResponse(serializer_return.data, safe=False, status=201)


@csrf_exempt
def create_creature_to_owner(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CreateCreatureSerializer(data=data)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        new_creature = Creature(
            name=data['name'],
            age=data['age'],
            breed=data['breed'],
            color_pattern=data['color_pattern'],
            owner=user
        )
        new_creature.save()

        serializer_return = GetCreatureSerializer(new_creature)
        return JsonResponse(serializer_return.data, safe=False, status=201)

@csrf_exempt
def get_own_creatures(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    serializer = GetOwnCreatures(user.get_own_creatures)
    return JsonResponse(serializer.data)


@csrf_exempt
def rate_creature(request, id, creature_id):
    try:
        user = User.objects.get(id=id)
        creature = Creature.objects.get(id=creature_id)
    except User.DoesNotExist or Creature.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = RateCreatureSerializer(data=data)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        new_rating = Rating(
            creature=creature,
            pub_date=data['pub_date'],
            user=user,
            comment=data['comment'],
            rating=data['rating']
        )
        new_rating.save()

        serializer_return = GetCreatureRatingSerializer(new_creature)
        return JsonResponse(serializer_return.data, safe=False, status=201)
