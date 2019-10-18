from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from creatder.decorators import is_authorized
from creatder.models import (
    Creature, Review, User, Token, PasswordResetToken, CreateAccountToken
    )
from creatder.serializers import (GetCreatureSerializer,
    CreateCreatureSerializer, GetUserSerializer, CreateUserSerializer,
    UpdateUserSerializer, GetOwnCreatures, RateCreatureSerializer,
    UpdateCreatureSerializer
    # GetCreatureRatingSerializer)
    )
from creatder.services import (
    send_password_reset_mail, check_token_validity, send_user_register_mail,
    MinimumLengthValidator, NumericPasswordValidator)


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
    List all users or add a user.
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
            email=data['email'],
            about_myself=data['about_myself']
        )
        new_user.set_password(data['password'])  # also saves the instance

        serializer_return = GetUserSerializer(new_user)
        return JsonResponse(serializer_return.data, safe=False, status=201)


@csrf_exempt
def user_details(request, id):
    """
    Retrieve, update or delete a user.
    """
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = GetUserSerializer(user)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        # No changing passwords here!
        data = JSONParser().parse(request)
        serializer = UpdateUserSerializer(user, data=data)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)
        user.name = data['name']
        user.login = data['login']
        user.email = data['email']
        user.about_myself = data['about_myself']
        user.save()

        serializer_return = GetUserSerializer(user)
        return JsonResponse(serializer_return.data, safe=False)

    elif request.method == 'DELETE':
        user.delete()
        return HttpResponse(status=204)


@csrf_exempt
def creature_details(request, id):
    """
    Retrieve, update or delete a user.
    """
    try:
        creature = Creature.objects.get(id=id)
    except Creature.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = GetCreatureSerializer(creature)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = UpdateCreatureSerializer(creature, data=data)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)
        creature.name = data['name']
        creature.age = data['age']
        creature.sex = data['sex']
        creature.breed = data['breed']
        creature.color_pattern = data['color_pattern']
        creature.crossed_rainbow_bridge = data['crossed_rainbow_bridge']
        creature.save()

        serializer_return = GetCreatureSerializer(creature)
        return JsonResponse(serializer_return.data, safe=False)

    elif request.method == 'DELETE':
        creature.delete()
        return HttpResponse(status=204)


@csrf_exempt
def create_creature_to_owner(request, id):
    """
    Create new creature owned by registered user.
    """
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
            sex=data['sex'],
            breed=data['breed'],
            color_pattern=data['color_pattern'],
            owner=user
        )
        new_creature.save()

        serializer_return = GetCreatureSerializer(new_creature)
        return JsonResponse(serializer_return.data, safe=False, status=201)

@csrf_exempt
def creatures(request, id):
    # change name to get_user_creaaures
    """
    Retrieve users creatures.
    """
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    serializer = GetOwnCreatures(user.creatures)
    return JsonResponse(serializer.data)


# TODO: Only allow user to vote once on a creature; if they already voted
# update the value on the existing vote
@is_authorized
@csrf_exempt
def rate_creature(request, creature_id):
    """
    Rate a creature, also possible to add a comment.
    """
    try:
        creature = Creature.objects.get(id=creature_id)
    except Creature.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = RateCreatureSerializer(data=data)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        try:
            user = User.objects.get(id=data['user_id'])
        except Creature.DoesNotExist:
            return HttpResponse(status=404)

        review = Review.objects.filter(
            user__id=user.id, creature__id=creature.id).first()
        if review:
            review.comment = data['comment']
            review.rating = data['rating']
        else:
            review = Review(
                creature=creature,
                user=user,
                comment=data['comment'],
                rating=data['rating']
            )
        review.save()

        serializer_return = GetCreatureSerializer(creature)
        return JsonResponse(serializer_return.data, safe=False, status=201)


@csrf_exempt
def user_ratings(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = GetUserRatingsSerializer(user)
        return JsonResponse(serializer.data)


@csrf_exempt
def login(request):
    """
    Login a user.
    """
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = LoginSerializer(data=data)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        user = User.objects.get(email=data['email'])
        token = Token(user_id=user.id)
        token.save()
        serializer_return = TokenSerializer(token)
        return JsonResponse(serializer_return.data, safe=False, status=201)


@is_authorized
@csrf_exempt
def logout(request):
    """
    Logout a user.
    """
    if request.method == 'GET':
        result = request.META['HTTP_AUTHORIZATION']
        user_id = result.split(':')[0]
        uuid = result.split(':')[1]
        token = Token.objects.get(uuid=uuid)
        token.is_expired = True
        token.save()
        return HttpResponse(status=204)


@csrf_exempt
def register_request_view(request):
    """
    Register request from a user.
    """
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = RegisterRequestSerializer(data=data)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        token = CreateAccountToken(email=data['email'])
        token.save()
        send_user_register_mail(data['email'], str(token.uuid))
        serializer_return = RegisterTokenSerializer(token)
        return JsonResponse(serializer_return.data, safe=False, status=201)


@csrf_exempt
def register_view(request, token_uuid):
    """
    Register a user.
    """
    if request.method == 'POST':
        check_result = check_token_validity(CreateAccountToken, token_uuid)
        if check_result:
            return JsonResponse(check_result, status=403)

        else:
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
def password_reset_request(request):
    """
    Password reset request from a user.
    """
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PasswordResetRequestSerializer(data=data)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        user = User.objects.get(email=data['email'])
        token = PasswordResetToken(user=user)
        token.save()
        send_password_reset_mail(data['email'], str(token.uuid))
        serializer_return = PasswordResetTokenSerializer(token)
        return JsonResponse(serializer_return.data, safe=False, status=201)


@csrf_exempt
def reset_password_view(request, token_uuid):
    """
    Reset users password.
    """
    if request.method == 'POST':
        check_result = check_token_validity(PasswordResetToken, token_uuid)
        if check_result:
            return JsonResponse(check_result, status=400)

        token = PasswordResetToken.objects.get(uuid=token_uuid)
        user = token.user
        data = JSONParser().parse(request)
        serializer = PasswordUserSerializer(user, data=data)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)
        user.set_password(data['password'])  # also saves the instance
        serializer_return = GetUserSerializer(user)
        return JsonResponse(serializer_return.data, safe=False, status=201)
