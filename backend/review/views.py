from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ReviewSerializer
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Review

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

class ReviewView(APIView):
    def post(self, request):
        review_serializer = ReviewSerializer(data=request.data)
        if review_serializer.is_valid():
            review_serializer.save()
            return Response(review_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(review_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, **kwargs):
        if kwargs.get('id') is None:
            review_queryset = Review.objects.all()
            review_queryset_serializer = ReviewSerializer(
                review_queryset, many=True)
            return Response(review_queryset_serializer.data, status=status.HTTP_200_OK)
        else:
            review_id = kwargs.get('id')
            review_serializer = ReviewSerializer(Review.objects.get(pk=review_id))
            return Response(review_serializer.data, status=status.HTTP_200_OK)

    def put(self, request, **kwargs):
        if kwargs.get('id') is None:
            return Response("fail", status=status.HTTP_400_BAD_REQUEST)
        else:
            review_id = kwargs.get('id')
            review_object = Review.objects.get(id=review_id)
            update_review_serializer = ReviewSerializer(review_object, data=request.data)
            if update_review_serializer.is_valid():
                update_review_serializer.save()
                return Response(update_review_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, **kwargs):
        if kwargs.get('id') is None:
            return Response("invalid delete request", status=status.HTTP_400_BAD_REQUEST)
        else:
            review_id = kwargs.get('id')
            review_object = Review.objects.get(id=review_id)
            review_object.delete()
            return Response("delete success", status=status.HTTP_200_OK)