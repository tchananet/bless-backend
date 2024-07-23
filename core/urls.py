from django.urls import include, path
from . import views
from django.conf import settings
from .views import tafiya, bless, facture, intro, facturation
# from views import

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

## Bless computer routs
router.register(r'messages',bless.MessageViewSet)
router.register(r'team',bless.TeamViewSet)
router.register(r'services',bless.ServiceViewSet)


#tafiya routes
router.register(r'products',tafiya.ProductViewSet)
router.register(r'category',tafiya.CategoryViewSet) 

#facture routes
router.register(r'transactions',facture.StockTransatcionViewSet) 
router.register(r'sales',facture.SalesViewSet) 

#factuation
router.register(r'facturation-categorie', facturation.CategorieViewSet)
router.register(r'facturation-produits', facturation.ProduitViewSet)
router.register(r'facturation-cateproduits', facturation.CategorieProduitViewSet, basename='categories')
router.register(r'facturation-vente', facturation.VenteViewSet)
router.register(r'facturation-sortie', facturation.SortieViewSet)
router.register(r'facturation-brouillard', facturation.BrouillardCaisseViewSet)

# router.register(r'enregistrer',facturation.RegisterUserView, 'Utilisateur') 

urlpatterns = [
    path('', intro.getDate),
    path('post/', intro.postData),

    # Bless
    path('service_list/', bless.ServiceList.as_view()),
    path('team_list/', bless.TeamList.as_view()),

    # Tafyia
    path('product_list/', tafiya.ProductList.as_view()),
    path('category_list/', tafiya.CategoryList.as_view()),

    # Sales
    path('transaction_list/', facture.StockTransactionList.as_view()),
    path('sales_list/', facture.SalesList.as_view()),
    path("utilisateur", facturation.UserView.as_view() ),
    path("register", facturation.RegisterUserView.as_view() ),
    path("login", facturation.UserLoginView.as_view() ),
    path("login-token", facturation.CustomAuthToken.as_view() ),
    path("register-token", facturation.TokenRegisterView.as_view() ),
    path("facturation-vente-total", facturation.TotalVentesView.as_view() ),
    path("facturation-sortie-total", facturation.TotalSortiesView.as_view() ),
    path("facturation-net-total", facturation.TotalNetView.as_view() ),
    path('', include(router.urls)),

    #others
    path('url_repeater/', intro.url_repeater),
]

# router.register(r'utilisateurs',facturation.UserView) 
# 'facturation-vente-total', facturation.TotalVentesView