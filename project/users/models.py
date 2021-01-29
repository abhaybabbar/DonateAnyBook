from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Order(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=20)
    pincode = models.CharField(max_length=6)
    name = models.CharField(max_length=40)
    email = models.EmailField(max_length=254)
    number = models.CharField(max_length=10)
    book_title = models.CharField(max_length=80)
    book_author = models.CharField(max_length=80)
    status = models.BooleanField(default=False)
    coupon = models.BooleanField(default=False)
    def __str__(self):
        return self.book_title
     