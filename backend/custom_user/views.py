from django.shortcuts import render
from rest_framework import generics
# Create your views here.
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer, JSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings

from custom_user.models import UserManager, User
from custom_user.serializers import UserSerializer, UpdateUserSerializer, UserLoginSerializer


class CreateView(generics.GenericAPIView):
    queryset = User.objects.all()
    # api_view("POST")
    permission_classes(AllowAny, )
    serializer_class = UserSerializer

    def post(self, request, **kwargs):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.create(user_serializer.data)
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

JWT_DECODE_HANDLER = api_settings.JWT_DECODE_HANDLER

validation_error_message = "validation error"

class ModifyView(generics.UpdateAPIView):
    api_view(['PUT'])
    permission_classes([IsAuthenticated])
    authentication_classes((JSONWebTokenAuthentication,))
    queryset = User.objects.all()
    serializer_class = UpdateUserSerializer

    def put(self, request, **kwargs):
        if kwargs.get('id') is None:
            return Response("fail", status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                get_id = kwargs.get('id')
                token = request.headers.get("Authorization").split()[1]
                user = JWT_DECODE_HANDLER(token)
                if user['user_id'] == get_id:
                    user_obj = User.objects.get(id=get_id)
                    print(user_obj)
                    update_user_serializer = UserSerializer(user_obj, data=request.data)
                    if update_user_serializer.is_valid():
                        update_user_serializer.save()
                        return Response(update_user_serializer.data, status=status.HTTP_202_ACCEPTED)
                    else:
                        return Response("Invalid request", status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response("Invalid request", status=status.HTTP_400_BAD_REQUEST)
            except ValidationError as v:
                print(validation_error_message, v)
                return Response(validation_error_message, status=status.HTTP_400_BAD_REQUEST)


class DeleteView(generics.DestroyAPIView):
    api_view(['DELETE'])
    permission_classes([IsAuthenticated, ])
    authentication_classes((JSONWebTokenAuthentication,))
    def delete(self, request, **kwargs):
        if kwargs.get('id') is None:
            return Response("fail", status=status.HTTP_400_BAD_REQUEST)
        else:
            get_id = kwargs.get('id')
            # values = request.META
            # for value in values:
                # print(value)
            # headers = request.headers
            # for header in headers:
            #     print(header)
            token = request.headers.get("Authorization").split()[1]
            try:
                user = JWT_DECODE_HANDLER(token)
                print(user)
                if user['user_id'] == get_id:
                    user_obj = User.objects.get(id=get_id)
                    user_obj.delete()
                else:
                    return Response("Invalid Username", status=status.HTTP_400_BAD_REQUEST)
            except ValidationError as v:
                print(validation_error_message, v)
                return Response(validation_error_message, status=status.HTTP_400_BAD_REQUEST)
            return Response("delete success", status=status.HTTP_202_ACCEPTED)

class GetIDView(generics.RetrieveAPIView):
    api_view(['GET'])
    permission_classes([IsAuthenticated, ])
    authentication_classes((JSONWebTokenAuthentication,))
    def get(self, request):
        token = request.headers.get("Authorization").split()[1]
        try:
            user = JWT_DECODE_HANDLER(token)
            return Response(user['user_id'], status=status.HTTP_200_OK)
        except ValidationError as v:
            print(validation_error_message, v)
            return Response(validation_error_message, status=status.HTTP_400_BAD_REQUEST)

class LoginView(generics.GenericAPIView):
    api_view(['POST'])
    permission_classes(AllowAny, )
    serializer_class = UserLoginSerializer
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)
        if serializer.validated_data['email'] == "None":
            return Response({'message': 'fail'}, status=status.HTTP_200_OK)

        response = {
            'success': 'True',
            'user_id': serializer.data['id'],
            'token': serializer.data['token']
        }
        return Response(response, status=status.HTTP_200_OK)


