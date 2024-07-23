from rest_framework import serializers
from ..models.models import Data, Service, Team, Message, Product, Category, StockTransaction, Sale

class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model=Data
        fields = ('name', 'description') 

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Service
        fields = ('name', 'description')

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model=Team
        fields = ('name', 'position', 'image', 'socials', 'description') 


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model=Message
        fields = ('name', 'email', 'message', 'phone') 





