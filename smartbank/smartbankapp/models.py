from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    role = models.CharField(max_length=20, default='customer')

class Customer(models.Model):
    customer_name = models.CharField(max_length=50)
    email = models.EmailField(null=True, blank=True)
    id_type = models.CharField(max_length=20)
    id_document = models.FileField(upload_to='kyc/id_docs/')
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    created_by = models.CharField(max_length=50, null=True, blank=True)
    updated_by = models.DateTimeField(null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=1)
    cus_status = models.CharField(max_length=20, default=1)

class CustomerAccount(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=15, unique=True)
    account_type = models.CharField(max_length=20,default='savings')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    kyc_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=1)
