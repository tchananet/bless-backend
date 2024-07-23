from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet  
from rest_framework.views import APIView
# from .models import Data
from ..models.models import Data, Service, Team, Message 
from ..serializers.serializers import DataSerializer, ServiceSerializer, TeamSerializer, MessageSerializer 

# Create your views here.
@api_view(['GET'])
def getDate(request):
    app = Data.objects.all()
    serializer = DataSerializer(app, many=True)
    return Response(serializer.data)

# Create your views here.
@api_view(['POST'])
def postData(request):
    serialiser = DataSerializer(data=request.data)
    if serialiser.is_valid():
        serialiser.save()
        return Response(serialiser.data)
    return Response()

class ServiceViewSet(ModelViewSet):
    serializer_class = ServiceSerializer
    queryset = Service.objects.all() 

class TeamViewSet(ModelViewSet):
    serializer_class = TeamSerializer
    queryset = Team.objects.all() 

class MessageViewSet(ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all() 



class ServiceList(APIView):
    def get(self, request):
        services = Service.objects.all()
        serializer =ServiceSerializer(services, many=True)
        return Response(serializer.data)

class TeamList(APIView):
    def get(self, request):
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)

    # def post(self, request, format=None):
    #     serializer =ServiceSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)