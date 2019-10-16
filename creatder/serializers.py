from rest_framework import serializers

from creatder.models import Creature, Review, User


class GetUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(
        required=True, allow_blank=False, max_length=255)
    login = serializers.CharField(
        required=True, allow_blank=False, max_length=255)
    email = serializers.EmailField(
        required=True, allow_blank=False)
    about_myself = serializers.CharField(
        required=False, allow_blank=True, max_length=255)
    # see if putting "creatures" here works


class CreateUserSerializer(serializers.Serializer):
    name = serializers.CharField(
        required=True, allow_blank=False, max_length=255)
    login = serializers.CharField(
        required=True, allow_blank=False, max_length=255)
    email = serializers.EmailField(
        required=True, allow_blank=False)
    about_myself = serializers.CharField(
        required=False, allow_blank=True, max_length=255)
    password = serializers.CharField(
        required=True, allow_blank=False, max_length=255)
    password_repeat = serializers.CharField(
        required=True, allow_blank=False, max_length=255)

    def validate(self, data):
        if data['password'] != data['password_repeat']:
            raise serializers.ValidationError('Passwords did not match.')
        # elif not MinimumLengthValidator.validate(data['password']):
        #     raise serializers.ValidationError(
        #         'Passwords must have at least 8 characters')
        # elif not NumericPasswordValidator.validate(data['password']):
        #     raise serializers.ValidationError(
        #         'Password must contain at least 1 digit')

        user = User.objects.filter(email=data['email']).first()
        if user:
            raise serializers.ValidationError(
                'User with this email already exists.')
        return data


class UpdateUserSerializer(serializers.Serializer):
    name = serializers.CharField(
        required=True, allow_blank=False, max_length=255)
    login = serializers.CharField(
        required=True, allow_blank=False, max_length=255)
    email = serializers.EmailField(
        required=True, allow_blank=False)
    about_myself = serializers.CharField(
        required=False, allow_blank=True, max_length=255)

    def validate(self, data):
        user = User.objects.filter(email=data['email']).first()
        if user and user.id != self.instance.id:
            raise serializers.ValidationError(
                'User with this email already exists.')
        return data


class CreateCreatureSerializer(serializers.Serializer):
    name = serializers.CharField(
        required=True, allow_blank=False, max_length=255)
    age = serializers.IntegerField(max_value=20, min_value=0)
    sex = serializers.CharField(
        required=True, allow_blank=False, max_length=255)
    breed = serializers.CharField(
        required=True, allow_blank=False, max_length=255)
    color_pattern = serializers.CharField(
        required=True, allow_blank=False, max_length=255)
    crossed_rainbow_bridge = serializers.BooleanField(
        required=False)
    owner = GetUserSerializer(many=False)


class UpdateCreatureSerializer(serializers.Serializer):
    name = serializers.CharField(
        required=True, allow_blank=False, max_length=255)
    age = serializers.IntegerField(max_value=20, min_value=0)
    sex = serializers.CharField(
        required=True, allow_blank=False, max_length=255)
    breed = serializers.CharField(
        required=True, allow_blank=False, max_length=255)
    color_pattern = serializers.CharField(
        required=True, allow_blank=False, max_length=255)
    crossed_rainbow_bridge = serializers.BooleanField(
        required=False)


class GetCreatureSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(
        required=True, allow_blank=False, max_length=255)
    age = serializers.IntegerField(max_value=20, min_value=0)
    sex = serializers.CharField(
        required=True, allow_blank=False, max_length=255)
    breed = serializers.CharField(
        required=True, allow_blank=False, max_length=255)
    color_pattern = serializers.CharField(
        required=True, allow_blank=False, max_length=255)
    crossed_rainbow_bridge = serializers.BooleanField(
        required=False)
    average_rating = serializers.FloatField(read_only=True)
    owner = GetUserSerializer(many=False)


class GetOwnCreatures(serializers.Serializer):
    get_own_creatures = GetCreatureSerializer(many=True)


class RateCreatureSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    comment = serializers.CharField(
        required=False, allow_blank=True, max_length=255)
    rating=serializers.IntegerField(max_value=5, min_value=1)


# class GetCreatureRatingSerializer(serializers.Serializer):
#     creature = GetCreatureSerializer(many=False)
#     average_rating =
