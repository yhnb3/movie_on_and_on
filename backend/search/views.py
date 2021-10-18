from django.shortcuts import render

# Create your views here.
from jsonschema import ValidationError
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings

from .models import Search
from .serializers import SearchSerializer

JWT_DECODE_HANDLER = api_settings.JWT_DECODE_HANDLER
validation_error_message = "validation error"
class SaveSearchView(generics.CreateAPIView):
    permission_classes([IsAuthenticated])
    authentication_classes((JSONWebTokenAuthentication,))
    serializer_class = SearchSerializer
    def post(self, request):
        try:
            search_serializer = SearchSerializer(data=request.data)
            if search_serializer.is_valid():
                search_serializer.save()
            else:
                return Response("invalid data", status=status.HTTP_400_BAD_REQUEST)
            return Response("success", status=status.HTTP_200_OK)
        except ValidationError as v:
            print(validation_error_message, v)
            return Response(validation_error_message, status=status.HTTP_400_BAD_REQUEST)