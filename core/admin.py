from django.contrib import admin 
from .models.models import Data, Service, Image, Testimony, Message, Team, Product, Category, StockTransaction, Sale, InvoiceProducts, Invoice
# from .models.facturation import User, Categorie
# Register your models here.

admin.site.register(Data)
admin.site.register(Service)
admin.site.register(Team)
admin.site.register(Image)
admin.site.register(Testimony)
admin.site.register(Message) 
admin.site.register(Category) 
admin.site.register(Product) 
admin.site.register(StockTransaction) 
admin.site.register(Sale) 
admin.site.register(Invoice) 
admin.site.register(InvoiceProducts) 

