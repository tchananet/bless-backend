from rest_framework import serializers
from ..models.facturation import Categorie, Produit, Facturation, FacturationItem, Vente, Sortie, BrouillardCaisse
from django.contrib.auth import authenticate
from ..models.facturation import User
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'telephone', 'nom']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['telephone', 'nom', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(
            telephone=validated_data['telephone'],
            nom=validated_data['nom'],
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    telephone = serializers.CharField()
    password = serializers.CharField()
    

    def validate(self, data):
        print(data)
        user = authenticate(telephone=data['telephone'], password=data['password'])
        if user and user.is_active:
            print(user)
            return user
        raise serializers.ValidationError("Incorrect credentials")

class TokenLoginSerializer(serializers.Serializer):
    telephone = serializers.CharField()
    password = serializers.CharField()
    

    def validate(self, data):
        # print(data)
        user = authenticate(telephone=data['telephone'], password=data['password'])
        if user and user.is_active: 
            token, _ = Token.objects.get_or_create(user=user)
            return {
                'token': token.key,
                'user_id': user.pk,
                'telephone': user.telephone
            }
        raise serializers.ValidationError("Incorrect credentials")
    def create(self, validated_data):
        user = User.objects.create_user(
            telephone=validated_data['telephone'],
            nom=validated_data['nom'],
            password=validated_data['password']
        )
        return user
    
class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = ['id', 'designation', 'description']


class ProduitSerializer(serializers.ModelSerializer):
    categorie = CategorieSerializer(read_only=True)
    categorie_id = serializers.PrimaryKeyRelatedField(
        queryset=Categorie.objects.all(), source='categorie', write_only=True
    )

    class Meta:
        model = Produit
        fields = ['id', 'categorie', 'categorie_id', 'designation', 'prix', 'description']


class CategorieProductSerializer(serializers.ModelSerializer):
    produits = ProduitSerializer(many=True, read_only=True)
    class Meta:
        model = Categorie
        fields = ['id', 'designation', 'description', 'produits']

class FacturationItemSerializer(serializers.ModelSerializer):
    produit = ProduitSerializer(read_only=True)
    produit_id = serializers.PrimaryKeyRelatedField(
        queryset=Produit.objects.all(), source='produit', write_only=True
    )

    class Meta:
        model = FacturationItem
        fields = ['id', 'produit', 'produit_id', 'quantite']

class FacturationSerializer(serializers.ModelSerializer):
    items = FacturationItemSerializer(many=True, read_only=True)

    class Meta:
        model = Facturation
        fields = ['id', 'nom', 'address', 'numero', 'items']

class VenteSerializer(serializers.ModelSerializer):
    date_cree = serializers.DateTimeField(read_only=True)
    produit = ProduitSerializer(read_only=True)
    produit_id = serializers.PrimaryKeyRelatedField(
        queryset=Produit.objects.all(), source='produit', write_only=True
    )
    vendeur = serializers.ReadOnlyField(source='vendeur.nom')

    class Meta:
        model = Vente
        fields = ['id', 'produit', 'produit_id', 'montant', 'prix', 'quantite', 'vendeur', 'date_cree']

class SortieSerializer(serializers.ModelSerializer):
    date_cree = serializers.DateTimeField(read_only=True)
    class Meta:
        model = Sortie
        fields = ['id', 'libelle', 'tiers', 'montant', 'date_cree']

class BrouillardCaisseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrouillardCaisse
        fields = ['id', 'libelle', 'tiers', 'montant', 'type', 'solde', 'observation']
    def update(self, instance, validated_data):
        # Appeler la méthode reset_balance() du modèle
        instance.reset_balance(validated_data['solde_initial'])
        return instance