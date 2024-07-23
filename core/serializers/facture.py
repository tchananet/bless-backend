from rest_framework import serializers
from ..models.models import Data, Service, Team, Message, Product, Category, StockTransaction, Sale

 

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields = ('id', 'designation', 'description') 

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields = ('id', 'designation', 'description', 'category', 'price')  
        
class StockTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model=StockTransaction
        fields = ('id', 'label', 'beneficiary', 'sales', 'expenses', 'observation', 'created_at') 

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = '__all__'





