from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet  
from rest_framework.views import APIView
# from .models import Data
from ..models.models import  Product, Category, StockTransaction, Sale
from ..serializers.facture import  ProductSerializer, CategorySerializer, StockTransactionSerializer, SaleSerializer
 
# Viewsets

class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all() 

class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all() 


class StockTransatcionViewSet(ModelViewSet):
    serializer_class = StockTransactionSerializer
    queryset = StockTransaction.objects.all() 


class SalesViewSet(ModelViewSet):
    serializer_class = SaleSerializer
    queryset = Sale.objects.all() 
 

    
class CategoryList(APIView):
    def get(self, request):
        teams = Category.objects.all()
        serializer = CategorySerializer(teams, many=True)
        return Response(serializer.data)
    

class SalesList(APIView):
    def get(self, request):
        sales = Sale.objects.all()
        serializer = SaleSerializer(sales, many=True)
        return Response(serializer.data)


class StockTransactionList(APIView):
    def get(self, request):
        transaction = StockTransaction.objects.all()
        serializer = StockTransactionSerializer(transaction, many=True)
        return Response(serializer.data)