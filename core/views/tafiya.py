from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet  
from rest_framework.views import APIView
# from .models import Data
from ..models.models import  Product, Category
from ..serializers.facture import  ProductSerializer, CategorySerializer


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all() 

class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all() 


    
class CategoryList(APIView):
    def get(self, request):
        teams = Category.objects.all()
        serializer = CategorySerializer(teams, many=True)
        return Response(serializer.data)
    

class ProductList(APIView):
    def get(self, request):
        teams = Product.objects.all()
        serializer = ProductSerializer(teams, many=True)
        return Response(serializer.data)
