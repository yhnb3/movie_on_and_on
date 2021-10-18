from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_jwt.serializers import VerificationBaseSerializer
from rest_framework_jwt.settings import api_settings

from custom_user.models import User




class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            nickname=validated_data['nickname']
        )

    class Meta:
        model = User
        fields = ['email', 'password', 'nickname']


class UpdateUserSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        if 'email' in validated_data:
            instance.user.password = make_password(
                validated_data.get('email').get('password', instance.user.password)
            )
            instance.user.save()

    class Meta:
        model = User
        fields = '__all__'


from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

from django.contrib.auth.hashers import make_password
class UserLoginSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    email = serializers.EmailField(max_length=64)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        credentials = {
            'email': email,
            'password': password
        }
        user = authenticate(**credentials)
        if user is None:
            return {
                'email': 'None'
            }
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )
        return {
            'email': user.email,
            'id': user.pk,
            'token': jwt_token
        }

#
# class DeleteUserSerializer(serializers.ModelSerializer):
#     def delete(self, instance, validated_data):
#
#     class Meta:
#         model=User
#         fiel

