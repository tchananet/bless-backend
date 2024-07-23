from django.db import models
import uuid

# Create your models here. 

class Category(models.Model):
    description = models.CharField(max_length=200)
    designation = models.CharField(max_length=200) 
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.designation


class Product(models.Model):
    # id = models.IntegerField(primary_key=True, auto_created=True, unique=True)
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    designation = models.CharField(max_length=200)
    price = models.IntegerField(default=100)
    weight = models.IntegerField(default=1)
    stock = models.IntegerField(default=1)
    volume = models.IntegerField(default=10)
    image = models.CharField(max_length=300, blank=True) 
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, related_name='products_of')
    description = models.CharField(max_length=300)

    def __str__(self):
        return self.designation


class StockTransaction(models.Model):
    # no = models.AutoField(auto_created=True, editable=False)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    label = models.CharField(max_length=250)
    beneficiary = models.CharField(max_length=250)
    sales = models.IntegerField(blank=True, null=0)
    expenses = models.IntegerField(blank=True, null=0)
    observation = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True, auto_created=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)


class Sale(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(auto_now=True, editable=False)
    client = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    license_plate = models.CharField(max_length=20)
    gps_kit = models.BooleanField()
    sim_number = models.CharField(max_length=20)
    imei = models.CharField(max_length=20)
    seller = models.CharField(max_length=100)
    sale_type = models.CharField(max_length=100)
    quantity = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    advance = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    observation = models.CharField(max_length=100) 

class CashManagement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    label = models.CharField(max_length=250)
    beneficiary = models.CharField(max_length=250)
    sales = models.IntegerField(blank=True, null=0)
    expenses = models.IntegerField(blank=True, null=0)
    net = models.IntegerField(blank=True, null=0)
    observation = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True, auto_created=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)


class CashManagementDaily(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  
    sales_total = models.IntegerField(blank=True, null=0)
    expenses_total = models.IntegerField(blank=True, null=0)
    net_total = models.IntegerField(blank=True, null=0)
    amount = models.IntegerField(blank=True, null=0) 
    date = models.DateTimeField(auto_now=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, auto_created=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

class Invoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)    
    bill_no = models.CharField(max_length=250)
    firstName = models.CharField(max_length=250)
    lastName = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    phone = models.CharField(max_length=250)
    payment = models.CharField(max_length=250)
    seller = models.CharField(max_length=250)
    amount = models.IntegerField(blank=True, null=0) 
    created_at = models.DateTimeField(auto_now_add=True, auto_created=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False) 

    def __str__(self):
        return self.bill_no
    

class InvoiceProducts(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)   
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantiy = models.IntegerField()
    invoice = models.ForeignKey(to=Invoice, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, auto_created=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

class CurrentCash(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)   
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantiy = models.IntegerField()
    invoice = models.ForeignKey(to=Invoice, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, auto_created=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

  
data = [
  {
    "id": "46a96760-0a0c-11ef-ac66-0f758bea9c11",
    "price": 5200,
    "designation": "Miel",
    "description": "Miel Pur",
    "weight": 4,
    "volume": 4,
    "createdAt": "2024-05-04T11:48:51+00:00"
  },
  {
    "id": "ef1f7264-09fc-11ef-a444-0f758bea9c11",
    "price": 15000,
    "designation": "Huile Mayor",
    "description": "Huile de palme rafinee",
    "weight": 10,
    "volume": 12,
    "createdAt": "2024-05-04T09:59:02+00:00"
  }
]
    

"""
- Services
- Images
- Temoignage
	- nom
	- photo
	- temoigange
- formulaire de contac
- about us
- our team
	- name
	- photo
	- description
"""