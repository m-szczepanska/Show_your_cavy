from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser, FileUploadParser
from rest_framework.response import Response
from rest_framework import authentication, permissions, status


from creatder.decorators import is_authorized, is_authorized_photo
from creatder.models import (
    Creature, Review, User, Token, PasswordResetToken, CreateAccountToken, File
    )
from creatder.serializers import (GetCreatureSerializer,
    CreateCreatureSerializer, GetUserSerializer, CreateUserSerializer,
    UpdateUserSerializer, RateCreatureSerializer,GetUserRatingsSerializer,
    UpdateCreatureSerializer, RegisterTokenSerializer, RegisterRequestSerializer,
    TokenSerializer, LoginSerializer, PasswordResetRequestSerializer,
    PasswordResetTokenSerializer, PasswordUserSerializer,
    FileSerializer, SearchCreatureSerializer)

from creatder.services import (
    send_password_reset_mail, check_token_validity, send_user_register_mail,
    MinimumLengthValidator, NumericPasswordValidator, delete_pig_photo)


# @is_authorized
@csrf_exempt
def creature_list(request):
    """
    List all creatures.
    """
    if request.method == 'GET':
        creatures_all = Creature.objects.all()
        serializer = GetCreatureSerializer(creatures_all, many=True)
        return JsonResponse(serializer.data, safe=False)



@csrf_exempt
def creature_list_paginated(request, page=1):
    """
    List all creatures.
    Page size is 9 (hence magic 9s in the code).
    """
    # Ignore bad value for page and substitute 1
    if page < 1 or type(page) != int:
        page = 1

    if request.method == 'GET':
        creatures_all = Creature.objects.all()
        creature_count = creatures_all.count()
        # TODO: jeez fix this shit plis, miss; this is bad every 9 pigs
        # This shows on frontend so we start at 1
        if (creature_count % 9) == 0:
            max_page = (creature_count // 9)
        else:
            max_page = (creature_count // 9) + 1

        upper_limit = min([page * 9, creature_count])
        creatures = creatures_all[(page-1)*9:upper_limit]

        serializer = GetCreatureSerializer(creatures, many=True)
        resp = {
            "objects": serializer.data,
            "page": page,
            "max_page": max_page
        }

        return JsonResponse(resp, safe=False)


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

# @is_authorized
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
        data = JSONParser().parse(request)
        serializer = UpdateUserSerializer(user, data=data)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)
        user.name = data['name']
        user.email = data['email']
        user.about_myself = data['about_myself']
        user.save()

        serializer_return = GetUserSerializer(user)
        return JsonResponse(serializer_return.data, safe=False)

    elif request.method == 'DELETE':
        user.delete()
        return HttpResponse(status=204)


# @is_authorized
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


@is_authorized
@csrf_exempt
def create_creature(request, user_id):
    """
    Create new creature owned by registered user.
    """
    try:
        user = User.objects.get(id=user_id)
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
            crossed_rainbow_bridge=data['crossed_rainbow_bridge'],
            owner=user
        )
        new_creature.save()

        serializer_return = GetCreatureSerializer(new_creature)
        return JsonResponse(serializer_return.data, safe=False, status=201)

@is_authorized
@csrf_exempt
def get_user_creatures(request, id):
    """
    Retrieve users creatures.
    """
    try:
        owner = User.objects.get(id=id)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    creatures = Creature.objects.filter(owner=owner)

    serializer = GetCreatureSerializer(creatures, many=True)
    return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def user_ratings(request, id):
    """
    Retrieve user ratings.
    """
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    get_user_ratings = Review.objects.filter(
        user__id=user.id)

    if request.method == 'GET':
        serializer = GetUserRatingsSerializer(get_user_ratings, many=True)
        return JsonResponse(serializer.data, safe=False)


# TODO: Only allow user to vote once on a creature; if they already voted
# update the value on the existing vote
@is_authorized
@csrf_exempt
def rate_creature(request, id):
    """
    Rate a creature, also possible to add a comment.
    """
    try:
        creature = Creature.objects.get(id=id)
    except Creature.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = RateCreatureSerializer(data=data)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        try:
            user = User.objects.get(id=data['user_id'])
        except User.DoesNotExist:
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
def login(request):
    """
    Login a user.
    """
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = LoginSerializer(data=data)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        user = User.objects.get(login=data['login'])
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
            print('good token')
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


@csrf_exempt
def search_creature(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SearchCreatureSerializer(data=data)

        creatures = Creature.objects.filter(
            Q(name__icontains=data['search_field']) |
            Q(breed__icontains=data['search_field'])
        )
        serializer_return = GetCreatureSerializer(creatures, many=True)
        return JsonResponse(serializer_return.data, safe=False, status=201)




class FileUploadView(APIView):
    """
    Retrieve all photos or upload a photo.
    """
    parser_class = (MultiPartParser, FormParser)

    @is_authorized_photo
    def get(self, request, creature_id, *args, **kwargs):
        try:
            creature = Creature.objects.get(id=creature_id)
        except Creature.DoesNotExist:
            return HttpResponse(status=404)

        files = File.objects.filter(creature__id=creature.id)
        file_serializer = FileSerializer(files, many=True)
        return Response(file_serializer.data)

    def post(self, request, creature_id, *args, **kwargs):

        try:
            creature = Creature.objects.get(id=creature_id)
        except Creature.DoesNotExist:
            return HttpResponse(status=404)
        # Weird stuff; has to be 'creture' field for it's integer value
        request.data.update({'creature': creature.id})

        file_serializer = FileSerializer(data=request.data)

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileUploadDetails(APIView):
    """
    Retrieve, update or delete a photo instance.
    """
    # @is_authorized
    def get_object(self, id, creature_id):
        # import pdb; pdb.set_trace()
        try:
            creature = Creature.objects.get(id=id)
        except Creature.DoesNotExist:
            return HttpResponse(status=404)

        try:
            return File.objects.filter(
                id=id, creature__id=creature.id).first()
        except File.DoesNotExist:
            return HttpResponse(status=404)

    # @is_authorized
    def get(self, request, id, creature_id):
        file = self.get_object(id, creature_id)
        serializer = FileSerializer(file)
        return Response(serializer.data)

    # @is_authorized
    # def put(self, request, id, creature_id):
    #     file = self.get_object(id, creature_id)
    #     serializer = FileSerializer(file, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @is_authorized
    def delete(self, request, id, creature_id, format=None):
        try:
            file = File.objects.filter(id=id, creature__id=creature_id).first()
        except File.DoesNotExist:
            return HttpResponse(status=404)

        file.delete()
        delete_pig_photo(file)
        return Response(status=status.HTTP_204_NO_CONTENT)
