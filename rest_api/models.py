from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self,username,password,**extra_fields):
        if not username:
            raise ValueError("Username sholud be provided")
        user=self.model(username=username,**extra_fields)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self,username,password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        return self.create_user(username,password,**extra_fields)
class User(AbstractBaseUser):
    id=models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=30,unique=True)
    email= models.EmailField(max_length=100,unique=True)
    mobile_number = models.CharField(max_length=15)
    password=models.CharField(max_length=100)
    USERNAME_FIELD='username'
    objects=UserManager()

class Products(models.Model):
    name= models.CharField(max_length=200)
    image=models.TextField()
    brand= models.CharField(max_length=100)
    shipping=models.TextField(null=True, blank=True)
    description= models.TextField(null=True, blank=True)
    price= models.FloatField()
    category= models.CharField(max_length=200)
    featured= models.BooleanField(default=False)
    active= models.BooleanField(default=True)
    created= models.DateTimeField(auto_now_add=True)
    class Meta:
        indexes=[
            models.Index(fields=["name"],name="name-index"),
            models.Index(fields=["brand","category"],name="brand-category-index")
        ]

class Order(models.Model):
    user= models.IntegerField()
    order_number= models.CharField(max_length=100)
    order_date= models.DateTimeField(auto_now_add=True)

class OrderItems(models.Model):
    order=models.IntegerField() # orderID
    product=models.IntegerField()#productID
    quantity= models.IntegerField()
    price= models.DecimalField(max_digits=10, decimal_places=2)

class Review(models.Model):
    product=models.IntegerField()
    user= models.IntegerField()
    rate= models.DecimalField(max_digits=2, decimal_places=2)
    review=models.CharField(max_length=100)
    created= models.DateTimeField(auto_now_add=True)
    active= models.BooleanField(default=True)

class BillingAddress(models.Model):
    oreder= models.IntegerField(unique=True)
    address= models.TextField()
    city= models.CharField(max_length=100)

class Coupan(models.Model):
    code= models.CharField(max_length=100)
    discount= models.DecimalField(max_digits=2, decimal_places=2)
    orders=models.ManyToManyField(Order)