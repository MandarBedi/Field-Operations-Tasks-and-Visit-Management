from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class TestList(APIView):
    def get(self, request):
        data = {
            "message": "Connection Successful!",
            "status": "Django is talking to React",
            "items": [1, 2, 3]
        }
        return Response(data, status=status.HTTP_200_OK)
