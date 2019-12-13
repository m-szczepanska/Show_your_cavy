import functools

from django.http import HttpResponse
from django.http import JsonResponse
from creatder.models import Token


def uppercase(func):
    @functools.wraps(func)
    def wrapper():
        return func().upper()
    return wrapper


def is_authorized(func):
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        try:
            result = request.META.get('HTTP_AUTHORIZATION')
            if not result:
                return JsonResponse({"error":"Wrong header"}, status=400)
            # {'HTTP_AUTHORIZATION': 'ID_PLAYER:UUID_TOKEN'}
            result_split = result.split(':')
            if not result_split:
                return JsonResponse({"error":"Bad credentials"}, status=400)
            user_id = result_split[0]
            uuid = result_split[1]
            token = Token.objects.get(uuid=uuid)
            if token.user_id != int(user_id):
                print('Wrong user id')
                return JsonResponse({"error":"Wrong user id"}, status=401)
        except Token.DoesNotExist:
            return JsonResponse({"error":"Token doesn't exist"}, status=401)

        return func(request, *args, **kwargs)
    return wrapper


def is_authorized_photo(func):
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        try:
            result = request.request.META.get('HTTP_AUTHORIZATION')
            if not result:
                return JsonResponse({"error":"Wrong header"}, status=400)
            # {'HTTP_AUTHORIZATION': 'ID_PLAYER:UUID_TOKEN'}
            result_split = result.split(':')
            if not result_split:
                return HttpResponse(status=400)
            user_id = result_split[0]
            uuid = result_split[1]
            token = Token.objects.get(uuid=uuid)
            if token.user_id != int(user_id):
                print('Wrong user id')
                return JsonResponse({"error":"Wrong user id"}, status=401)
        except Token.DoesNotExist:
            return JsonResponse({"error":"Token doesn't exist"}, status=401)

        return func(request, *args, **kwargs)
    return wrapper
