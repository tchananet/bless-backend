from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Sum
from django.contrib.auth import login, logout
from ..models.facturation import User,  Categorie, Produit, Facturation, FacturationItem, Vente, Sortie, BrouillardCaisse
from ..serializers.facturation import LoginSerializer, TokenLoginSerializer, UserSerializer, RegisterSerializer, CategorieSerializer, ProduitSerializer, CategorieProductSerializer, FacturationSerializer, FacturationItemSerializer, VenteSerializer, SortieSerializer, BrouillardCaisseSerializer
from rest_framework.views import APIView

from rest_framework import generics 
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response  
    
class UserLoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print(request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        login(request, user)
        return Response({"message": "Login successful"})

class CustomAuthToken(generics.GenericAPIView):
    serializer_class = TokenLoginSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data )
        serializer.is_valid(raise_exception=True) 
        return Response( serializer.validated_data) 

class TokenRegisterView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'token': serializer.data['token'],
                'user_id': serializer.data['user_id'],
                'telephone': serializer.data['telephone']
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class UserView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self): 
       return self.request.user
    
class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    # permission_classes = [permissions.IsAuthenticated]

class ProduitViewSet(viewsets.ModelViewSet):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer
    # permission_classes = [permissions.IsAuthenticated]

class CategorieProduitViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieProductSerializer

class FacturationItemViewSet(viewsets.ModelViewSet):
    queryset = FacturationItem.objects.all()
    serializer_class = FacturationItemSerializer
    permission_classes = [permissions.IsAuthenticated]

class FacturationViewSet(viewsets.ModelViewSet):
    queryset = Facturation.objects.all()
    serializer_class = FacturationSerializer
    permission_classes = [permissions.IsAuthenticated]

# class VenteViewSet(viewsets.ModelViewSet):
#     queryset = Vente.objects.all()
#     serializer_class = VenteSerializer
#     permission_classes = [permissions.IsAuthenticated]

class VenteViewSet(viewsets.ModelViewSet):
    queryset = Vente.objects.all()
    serializer_class = VenteSerializer 
    def perform_create(self, serializer):
        # produit = Produit.objects.get(id=self.request.data?['produit'])
        serializer.save(vendeur=self.request.user)

    @action(detail=False, methods=['get'])
    def totaux_journaliers(self, request):
        today = timezone.now().date()
        entrees_total = Vente.objects.filter(date_cree__date=today).aggregate(total=Sum('montant'))['total'] or 0
        sorties_total = Sortie.objects.filter(date_cree__date=today).aggregate(total=Sum('montant'))['total'] or 0
        return Response({
            'entrees_total': entrees_total,
            'sorties_total': sorties_total
        })

    @action(detail=False, methods=['get'])
    def totaux_hebdomadaires(self, request):
        today = timezone.now().date()
        start_of_week = today - timezone.timedelta(days=today.weekday())
        end_of_week = start_of_week + timezone.timedelta(days=6)
        entrees_total = Vente.objects.filter(date_cree__date__gte=start_of_week, date_cree__date__lte=end_of_week).aggregate(total=Sum('prix'))['total'] or 0
        sorties_total = Sortie.objects.filter(date_cree__date__gte=start_of_week, date_cree__date__lte=end_of_week).aggregate(total=Sum('montant'))['total'] or 0
        return Response({
            'entrees_total': entrees_total,
            'sorties_total': sorties_total
        })

    @action(detail=False, methods=['get'])
    def totaux_mensuels(self, request):
        today = timezone.now().date()
        start_of_month = today.replace(day=1)
        end_of_month = start_of_month.replace(day=28) + timezone.timedelta(days=4)
        end_of_month = end_of_month - timezone.timedelta(days=end_of_month.day)
        entrees_total = Vente.objects.filter(date_cree__date__gte=start_of_month, date_cree__date__lte=end_of_month).aggregate(total=Sum('montant'))['total'] or 0
        sorties_total = Sortie.objects.filter(date_cree__date__gte=start_of_month, date_cree__date__lte=end_of_month).aggregate(total=Sum('montant'))['total'] or 0
        return Response({
            'entrees_total': entrees_total,
            'sorties_total': sorties_total
        })

class TotalVentesView(generics.GenericAPIView):
    serializer_class = VenteSerializer
    def get(self, request):
        debut = request.query_params.get('debut')
        fin = request.query_params.get('fin')
        date = request.query_params.get('date')

        ventes = Vente.objects.all()

        if debut and fin:
            ventes = ventes.filter(date_cree__range=[debut, fin])
        elif debut:
            ventes = ventes.filter(date_cree__gte=debut)
        elif fin:
            ventes = ventes.filter(date_cree__lte=fin)
        elif date:
            ventes = ventes.filter(date_cree__date=date) 
        
        total_jour = ventes.aggregate(Sum('montant'))['montant__sum']
        total_semaine = ventes.filter(date_cree__date__gte=datetime.now().date() - timedelta(days=6)).aggregate(Sum('montant'))['montant__sum']
        total_mois = ventes.filter(date_cree__year=datetime.now().year, date_cree__month=datetime.now().month).aggregate(Sum('montant'))['montant__sum']
        
        response = {
            "total_jour": total_jour if total_jour else 0,
            "total_semaine": total_semaine if total_semaine else 0,
            "total_mois": total_mois if total_mois else 0
        }
        
        return Response(response)

class TotalSortiesView(generics.GenericAPIView):
    serializer_class = SortieSerializer
    def get(self, request):
        debut = request.query_params.get('debut')
        fin = request.query_params.get('fin')
        date = request.query_params.get('date')

        sorties = Sortie.objects.all()

        if debut and fin:
            sorties = sorties.filter(date_cree__range=[debut, fin])
        elif debut:
            sorties = sorties.filter(date_cree__gte=debut)
        elif fin:
            sorties = sorties.filter(date_cree__lte=fin)
        elif date:
            sorties = sorties.filter(date_cree__date=date) 
        
        total_jour = sorties.aggregate(Sum('montant'))['montant__sum']
        total_semaine = sorties.filter(date_cree__date__gte=datetime.now().date() - timedelta(days=6)).aggregate(Sum('montant'))['montant__sum']
        total_mois = sorties.filter(date_cree__year=datetime.now().year, date_cree__month=datetime.now().month).aggregate(Sum('montant'))['montant__sum']
        
        response = {
            "total_jour": total_jour if total_jour else 0,
            "total_semaine": total_semaine if total_semaine else 0,
            "total_mois": total_mois if total_mois else 0
        }
        
        return Response(response)


class TotalNetView(generics.GenericAPIView):

    def get(self, request):
        debut = request.query_params.get('debut')
        fin = request.query_params.get('fin')
        date = request.query_params.get('date')

        ventes = Vente.objects.all()
        sorties = Sortie.objects.all()
        if debut and fin:
            ventes = ventes.filter(date_cree__range=[debut, fin])
            sorties = sorties.filter(date_cree__range=[debut, fin])
        elif debut:
            ventes = ventes.filter(date_cree__gte=debut)
            sorties = sorties.filter(date_cree__gte=debut)
        elif fin:
            ventes = ventes.filter(date_cree__lte=fin)
            sorties = sorties.filter(date_cree__lte=fin)
        elif date:
            ventes = ventes.filter(date_cree__date=date)
            sorties = sorties.filter(date_cree__date=date)
        
        total_ventes = ventes.aggregate(Sum('montant'))['montant__sum']
        total_sorties = sorties.aggregate(Sum('montant'))['montant__sum']

        total_net = total_ventes - total_sorties if total_ventes and total_sorties else 0

        response = {
            "total_net": total_net
        }

        if date:
            response["total_net_jour"] = total_net
        elif debut and fin:
            response["total_net_periode"] = total_net
        else:
            today = timezone.now().date()
            entrees_jour_total = Vente.objects.filter(date_cree__date=today).aggregate(total=Sum('montant'))['total'] or 0
            sorties_jour_total = Sortie.objects.filter(date_cree__date=today).aggregate(total=Sum('montant'))['total'] or 0

            start_of_week = today - timezone.timedelta(days=today.weekday())
            end_of_week = start_of_week + timezone.timedelta(days=6)
            entrees_week_total = Vente.objects.filter(date_cree__date__gte=start_of_week, date_cree__date__lte=end_of_week).aggregate(total=Sum('montant'))['total'] or 0
            sorties_week_total = Sortie.objects.filter(date_cree__date__gte=start_of_week, date_cree__date__lte=end_of_week).aggregate(total=Sum('montant'))['total'] or 0

            start_of_month = today.replace(day=1)
            end_of_month = start_of_month.replace(day=28) + timezone.timedelta(days=4)
            end_of_month = end_of_month - timezone.timedelta(days=end_of_month.day)
            entrees_month_total = Vente.objects.filter(date_cree__date__gte=start_of_month, date_cree__date__lte=end_of_month).aggregate(total=Sum('montant'))['total'] or 0
            sorties_month_total = Sortie.objects.filter(date_cree__date__gte=start_of_month, date_cree__date__lte=end_of_month).aggregate(total=Sum('montant'))['total'] or 0
            response = {
                'today': {'vente':entrees_jour_total, 'sorties':sorties_jour_total},
                'week': {'vente':entrees_week_total, 'sorties':sorties_week_total},
                'month': {'vente':entrees_month_total, 'sorties':sorties_month_total},
                        }
        
        return Response(response)
    
class TotalView(generics.GenericAPIView):
    today = timezone.now().date()
    def get(self, request):
        debut = request.query_params.get('debut')
        fin = request.query_params.get('fin')
        date = request.query_params.get('date')

        ventes = Vente.objects.all()
        sorties = Sortie.objects.all()

        if debut and fin:
            ventes = ventes.filter(date_cree__range=[debut, fin])
            sorties = sorties.filter(date_cree__range=[debut, fin])
        elif debut:
            ventes = ventes.filter(date_cree__gte=debut)
            sorties = sorties.filter(date_cree__gte=debut)
        elif fin:
            ventes = ventes.filter(date_cree__lte=fin)
            sorties = sorties.filter(date_cree__lte=fin)
        elif date:
            ventes = ventes.filter(date_cree__date=date)
            sorties = sorties.filter(date_cree__date=date)
        
        total_ventes = ventes.aggregate(Sum('montant'))['montant__sum']
        total_sorties = sorties.aggregate(Sum('montant'))['montant__sum']

        total_net = total_ventes - total_sorties if total_ventes and total_sorties else 0

        response = {
            "total_net": total_net
        }

        if date:
            response["total_net_jour"] = total_net
        elif debut and fin:
            response["total_net_periode"] = total_net
        else:
            # Calculer le total net pour la semaine en cours
            semaine_courante = datetime.now().date().isocalendar()[1]
            ventes_semaine = ventes.filter(date_cree__week=semaine_courante)
            sorties_semaine = sorties.filter(date_cree__week=semaine_courante)
            total_ventes_semaine = ventes_semaine.aggregate(Sum('montant'))['montant__sum']
            total_sorties_semaine = sorties_semaine.aggregate(Sum('montant'))['montant__sum']
            total_net_semaine = total_ventes_semaine - total_sorties_semaine if total_ventes_semaine and total_sorties_semaine else 0
            response["total_net_semaine"] = total_net_semaine

            # Calculer le total net pour le mois en cours
            mois_courant = datetime.now().month
            ventes_mois = ventes.filter(date_cree__month=mois_courant)
            sorties_mois = sorties.filter(date_cree__month=mois_courant)
            total_ventes_mois = ventes_mois.aggregate(Sum('montant'))['montant__sum']
            total_sorties_mois = sorties_mois.aggregate(Sum('montant'))['montant__sum']
            total_net_mois = total_ventes_mois - total_sorties_mois if total_ventes_mois and total_sorties_mois else 0
            response["total_net_mois"] = total_net_mois
        
        return Response(response)
    
class SortieViewSet(viewsets.ModelViewSet):
    queryset = Sortie.objects.all()
    serializer_class = SortieSerializer
    # permission_classes = [permissions.IsAuthenticated]

class BrouillardCaisseViewSet(viewsets.ModelViewSet):
    queryset = BrouillardCaisse.objects.all()
    serializer_class = BrouillardCaisseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        # Récupérer le dernier brouillard de caisse pour l'utilisateur connecté
        user = request.user
        last_entry = BrouillardCaisse.objects.filter(user=user).order_by('-created_at').first()

        # Mettre à jour le solde de la dernière entrée
        serializer = self.get_serializer(last_entry, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)