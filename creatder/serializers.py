from rest_framework import serializers

from creatder.models import (
    Creature, Review, User, Token, PasswordResetToken, CreateAccountToken,
    File)

from creatder.services import (MinimumLengthValidator,
    NumericPasswordValidator)


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
    email = serializers.EmailField(
        required=True, allow_blank=False)
    about_myself = serializers.CharField(
        required=False, allow_blank=True, max_length=255)

    def validate(self, data):
        user = User.objects.filter(email=data['email']).first()
        if user and user.id != self.instance.id:
            print(user.id, self.instance.id)
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
    creature_card_photo = serializers.CharField(
        required=True, allow_blank=False, max_length=255)
    pub_date = serializers.DateTimeField()
    owner = GetUserSerializer(many=False)


class RateCreatureSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    comment = serializers.CharField(
        required=False, allow_blank=True, max_length=200)
    rating=serializers.IntegerField(max_value=5, min_value=1)


class GetUserRatingsSerializer(serializers.Serializer):
    creature = GetCreatureSerializer(many=False)
    user_id = serializers.IntegerField()
    pub_date = serializers.DateTimeField()
    comment = serializers.CharField(
        required=False, allow_blank=True, max_length=200)
    rating=serializers.IntegerField(max_value=5, min_value=1)

class SearchCreatureSerializer(serializers.Serializer):
    search_field = serializers.CharField(
        required=False, allow_blank=True, max_length=40)


class LoginSerializer(serializers.Serializer):
    login = serializers.CharField(
        required=True, allow_blank=False, max_length=255)
    password = serializers.CharField(
        required=True, allow_blank=False, max_length=255)

    def validate(self, data):
        user = User.objects.filter(login=data['login']).first()
        if not user:
            raise serializers.ValidationError(
                'Login dosn\'t exists in the database')
        if not user.check_password(data['password']):
            raise serializers.ValidationError(
                'Password inncorect')
        return data


class TokenSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField()
    uuid = serializers.CharField(
        required=True, allow_blank=False)
    is_expired = serializers.BooleanField(read_only=True)


class RegisterRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(
            required=True, allow_blank=False)

    def validate(self, data):
        # TODO: make mail not case sensitive
        user = User.objects.filter(email=data['email']).first()
        if user:
            raise serializers.ValidationError(
                'Email already exists in the database')
        return data


class RegisterTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(
            required=True, allow_blank=False)
    created_at = serializers.DateTimeField()
    uuid = serializers.CharField(
        required=True, allow_blank=False)
    was_used = serializers.BooleanField(read_only=True)


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(
            required=True, allow_blank=False)

    def validate(self, data):
        user = User.objects.filter(email=data['email']).first()
        if not user:
            raise serializers.ValidationError(
                'Email does not exist in the database')
        return data


class PasswordResetTokenSerializer(serializers.Serializer):
    user = GetUserSerializer(many=False)
    created_at = serializers.DateTimeField()
    uuid = serializers.CharField(
        required=True, allow_blank=False)
    was_used = serializers.BooleanField(read_only=True)


class PasswordUserSerializer(serializers.Serializer):
    password = serializers.CharField(
        required=True, allow_blank=False, max_length=255)
    password_repeat = serializers.CharField(
        required=True, allow_blank=False, max_length=255)

    def validate(self, data):
        if data['password'] != data['password_repeat']:
            raise serializers.ValidationError('Passwords did not match.')
        elif not MinimumLengthValidator.validate(data['password']):
            raise serializers.ValidationError(
                'Passwords must have at least 8 characters')
        elif not NumericPasswordValidator.validate(data['password']):
            raise serializers.ValidationError(
                'Password must contain at least 1 digit')
        return data


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = "__all__"

# class FileSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     file = serializers.FileField(
#         max_length=None, allow_empty_file=False, use_url=False)
#     creature_id = serializers.IntegerField(read_only=True)
#
#     def create(self, validated_data):
#         return File.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.file = validated_data.get('file', instance.file)
#         instance.save()
#         return instance
