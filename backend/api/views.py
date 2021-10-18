from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BoardSerializer
from rest_framework import status
from .models import Board

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class BoardView(APIView):
    def post(self, request):
        board_serializer = BoardSerializer(data=request.data)
        if board_serializer.is_valid():
            board_serializer.save()
            return Response(board_serializer.data, status=201)
        else:
            return Response(board_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, **kwargs):
        if kwargs.get('id') is None:
            board_queryset = Board.objects.all()
            board_queryset_serializer = BoardSerializer(
                board_queryset, many=True)
            return Response(board_queryset_serializer.data, status=status.HTTP_200_OK)
        else:
            board_id = kwargs.get('id')
            board_serializer = BoardSerializer(Board.objects.get(pk=board_id))
            return Response(board_serializer.data, status=status.HTTP_200_OK)

    def put(self, request, **kwargs):
        if kwargs.get('id') is None:
            return Response("fail", status=status.HTTP_400_BAD_REQUEST)
        else:
            board_id = kwargs.get('id')
            board_object = Board.objects.get(id=board_id)
            update_board_serializer = BoardSerializer(board_object, data=request.data)
            if update_board_serializer.is_valid():
                update_board_serializer.save()
                return Response(update_board_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, **kwargs):
        if kwargs.get('id') is None:
            return Response("invalid delete request", status=status.HTTP_400_BAD_REQUEST)
        else:
            board_id = kwargs.get('id')
            board_object = Board.objects.get(id=board_id)
            board_object.delete()
            return Response("delete success", status=status.HTTP_200_OK)