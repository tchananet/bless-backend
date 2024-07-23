from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, telephone, nom, password):
        if not telephone:
            raise ValueError("L'utilisateur doit avoir un numéro de téléphone")
        if not nom:
            raise ValueError("L'utilisateur doit avoir un nom")
        
        user = self.model(
            telephone=telephone,
            nom=nom,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, telephone, nom, password):
        user = self.create_user(
            telephone=telephone,
            nom=nom,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    telephone = models.CharField(max_length=20, unique=True)
    nom = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='core_users',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='core_users',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
    )
    
    
    USERNAME_FIELD = 'telephone'
    REQUIRED_FIELDS = ['nom']

    objects = UserManager()

    def __str__(self):
        return self.telephone
    

class Categorie(models.Model):
    designation = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.designation

class Produit(models.Model):
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='produits')
    designation = models.CharField(max_length=100)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.designation

class Facturation(models.Model):
    nom = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    numero = models.CharField(max_length=20)
    produits = models.ManyToManyField(Produit, through='FacturationItem')

    def __str__(self):
        return f"{self.nom} - {self.numero}"

class FacturationItem(models.Model):
    facturation = models.ForeignKey(Facturation, on_delete=models.CASCADE, related_name='items')
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.IntegerField()



class TransactionType(models.TextChoices):
    SALE = 'SALE', 'Vente'
    REFUND = 'REFUND', 'Remboursement'
    PAYMENT = 'PAYMENT', 'Paiement'
    EXPENSE = 'EXPENSE', 'Dépense'


class Vente(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='ventes')
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    quantite = models.IntegerField()
    montant = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    # vendeur = models.CharField(max_length=100)
    vendeur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ventes')
    date_cree = models.DateTimeField(auto_now_add=True, auto_created=True, editable=False)
    date_modifie = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"Vente de {self.montant} par {self.vendeur.nom}"

    def save(self, *args, **kwargs):
        self.montant = self.prix * self.quantite
        super().save(*args, **kwargs)
        self.create_cash_register_transaction()

    def create_cash_register_transaction(self): 
        BrouillardCaisse.objects.create(
            libelle=f'vente de {self.produit.designation} par {self.vendeur.nom}',
            tiers=self.vendeur.nom, 
            type=TransactionType.SALE,
            montant=self.montant,
            date_cree=self.date_cree
        )

class Sortie(models.Model):
    libelle = models.CharField(max_length=100)
    tiers = models.CharField(max_length=100)
    montant = models.DecimalField(max_digits=10, decimal_places=0)
    date_cree = models.DateTimeField(auto_now_add=True, auto_created=True, editable=False)
    date_modifie = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"Sortie de {self.montant} par {self.tiers}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.create_cash_register_transaction()

    def create_cash_register_transaction(self): 
        BrouillardCaisse.objects.create(
            libelle=self.libelle,
            tiers=self.tiers,
            type=TransactionType.EXPENSE,
            montant=self.montant,
            date_cree=self.date_cree
        )

class BrouillardCaisse(models.Model):
    libelle = models.CharField(max_length=100)
    tiers = models.CharField(max_length=100)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=20)
    solde = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    solde_initial = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    observation = models.TextField(null=True, blank=True)
    date_cree = models.DateTimeField(auto_now_add=True, auto_created=True, editable=False)
    date_modifie = models.DateTimeField(auto_now=True, editable=False)

    def save(self, *args, **kwargs):
        # Calculer le nouveau solde
        previous_balance = BrouillardCaisse.objects.filter(date_cree__lt=self.date_cree).order_by('-date_cree').first()
        if previous_balance:
            new_balance = previous_balance.solde
            if new_balance is None:
                new_balance = 0
            if self.type == TransactionType.SALE:
                new_balance = self.montant + new_balance
            elif self.type == TransactionType.EXPENSE:
                new_balance = self.montant - new_balance
        else:
            new_balance = self.solde_initial
            if new_balance is None:
                new_balance = 0
            if self.type == TransactionType.SALE:
                new_balance = self.montant + new_balance
            elif self.type == TransactionType.EXPENSE:
                new_balance = self.montant - new_balance

        self.solde = new_balance

        # Appeler la méthode save() de la classe parente
        super().save(*args, **kwargs)

    def reset_balance(self, new_balance):
        # Récupérer la dernière entrée
        last_entry = BrouillardCaisse.objects.order_by('-date_cree').first()

        # Créer une copie de la dernière entrée
        new_entry = BrouillardCaisse.objects.create(
            tiers=last_entry.tiers,
            type=last_entry.type,
            montant=last_entry.montant,
            solde_initial=new_balance
        )

        # Enregistrer la nouvelle entrée
        new_entry.save()

        # Mettre à jour le solde initial de la dernière entrée
        last_entry.solde_initial = new_balance
        last_entry.save()